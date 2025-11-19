<template>
  <div class="dashboard manager-dashboard">
    <header class="dashboard-header">
      <div class="header-content">
        <h1>Tableau de bord - Manager</h1>
        <div class="user-info">
          <span class="user-name">{{ user.full_name }}</span>
          <span class="user-role">Manager</span>
          <button @click="handleLogout" class="btn btn-secondary">
            Déconnexion
          </button>
        </div>
      </div>
    </header>

    <main class="dashboard-content">
      <!-- Vue d'ensemble de l'équipe -->
      <section class="card team-overview">
        <h2>Mon Équipe</h2>
        <div v-if="loadingTeam" class="loading">Chargement...</div>
        <div v-else-if="!team" class="no-data">
          Aucune équipe assignée
        </div>
        <div v-else>
          <h3>{{ team.name }}</h3>
          <p>{{ team.description }}</p>
          <p class="team-size">{{ team.members?.length || 0 }} membres</p>
        </div>
      </section>

      <!-- Statistiques équipe -->
      <section class="card team-stats">
        <h2>Statistiques de l'équipe</h2>
        <div class="stats-grid">
          <div class="stat-item">
            <span class="stat-value">{{ presentToday }}</span>
            <span class="stat-label">Présents aujourd'hui</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ absentToday }}</span>
            <span class="stat-label">Absents</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ lateToday }}</span>
            <span class="stat-label">Retards</span>
          </div>
        </div>
      </section>

      <!-- Pointages du jour -->
      <section class="card today-clocks">
        <h2>Pointages d'aujourd'hui (Équipe)</h2>
        <div v-if="loadingClocks" class="loading">Chargement...</div>
        <div v-else-if="teamTodayClocks.length === 0" class="no-data">
          Aucun pointage aujourd'hui pour votre équipe
        </div>
        <table v-else class="data-table">
          <thead>
            <tr>
              <th>Employé</th>
              <th>Heure</th>
              <th>Type</th>
              <th>Statut</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="clock in teamTodayClocks" :key="clock.id">
              <td>{{ getUserName(clock) }}</td>
              <td>{{ formatTime(clock.timestamp) }}</td>
              <td>
                <span :class="['badge', getClockType(clock) === 'in' ? 'badge-success' : 'badge-danger']">
                  {{ getClockType(clock) === 'in' ? 'Arrivée' : 'Départ' }}
                </span>
              </td>
              <td>
                <span :class="['badge', getStatusClass(clock)]">
                  {{ getStatus(clock) }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </section>

      <!-- Liste des membres de l'équipe -->
      <section class="card team-members">
        <h2>Membres de l'équipe</h2>
        <div v-if="loadingTeam" class="loading">Chargement...</div>
        <div v-else-if="!team || !team.members || team.members.length === 0" class="no-data">
          Aucun membre dans l'équipe
        </div>
        <div v-else class="members-grid">
          <div v-for="member in team.members" :key="member.id" class="member-card">
            <div class="member-info">
              <h4>{{ member.first_name }} {{ member.last_name }}</h4>
              <p>{{ member.function || 'Employé' }}</p>
              <p class="member-email">{{ member.email }}</p>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import authService from '@/services/authService'
import api from '@/services/api'

export default {
  name: 'ManagerDashboard',
  setup() {
    const router = useRouter()
    const user = ref(authService.getCurrentUser() || {})
    const team = ref(null)
    const todayClocks = ref([])
    const loadingTeam = ref(false)
    const loadingClocks = ref(false)

    const teamMemberIds = computed(() => {
      if (!team.value || !team.value.members) return []
      // Les membres sont soit des IDs directs, soit des objets
      const ids = team.value.members.map(m => {
        // Si c'est un nombre ou une string, c'est l'ID directement
        if (typeof m === 'number' || typeof m === 'string') return Number(m)
        // Sinon c'est un objet, extraire l'ID
        return m.id || m.user_id || m.pk || m.employee_id
      })
      return ids.filter(id => id !== undefined && id !== null)
    })

    const teamTodayClocks = computed(() => {
      return todayClocks.value.filter(clock => {
        const clockUserId = clock.user_id || clock.user || clock.employee_id || clock.employee
        return teamMemberIds.value.includes(clockUserId)
      })
    })

    const presentToday = computed(() => {
      // Filtrer uniquement les pointages "in" (arrivée)
      const checkIns = teamTodayClocks.value.filter(c => {
        const type = c.clock_type || c.attendance_type || c.type
        return type === 'in' || type === 'IN'
      })
      const uniqueUsers = new Set(checkIns.map(c => c.user_id || c.user))
      return uniqueUsers.size
    })

    const absentToday = computed(() => {
      if (!team.value || !team.value.members) return 0
      return team.value.members.length - presentToday.value
    })

    const lateToday = computed(() => {
      return teamTodayClocks.value.filter(c => isLate(c)).length
    })

    const fetchTeam = async () => {
      loadingTeam.value = true
      try {
        // Récupérer l'équipe gérée par ce manager
        const response = await api.get('/teams')
        const teams = response.data.results || response.data
        team.value = teams.find(t => {
          // Essayer de matcher avec manager_id ou manager
          return t.manager_id === user.value.id || 
                 t.manager === user.value.id ||
                 String(t.manager_id) === String(user.value.id) ||
                 String(t.manager) === String(user.value.id)
        })
        if (team.value) {
          
          // Si les membres sont juste des IDs, récupérer leurs infos complètes
          if (team.value.members && team.value.members.length > 0 && typeof team.value.members[0] === 'number') {
            try {
              const usersResponse = await api.get('/users/')
              const allUsers = usersResponse.data.results || usersResponse.data || []
              // Remplacer les IDs par les objets utilisateurs complets
              team.value.members = team.value.members.map(memberId => {
                return allUsers.find(u => u.id === memberId) || { id: memberId }
              })
            } catch (e) {
              console.error('Erreur lors de la récupération des infos utilisateurs:', e)
            }
          }
        }
      } catch (error) {
        console.error('Erreur lors du chargement de l\'équipe:', error)
      } finally {
        loadingTeam.value = false
      }
    }

    const fetchTodayClocks = async () => {
      loadingClocks.value = true
      try {
        // Récupérer TOUS les pointages pour pouvoir filtrer ceux de l'équipe
        const response = await api.get('/attendance/', {
          params: {
            limit: 1000 // Augmenter la limite pour avoir tous les pointages récents
          }
        })
        
        // Extraire les pointages selon la structure de la réponse
        let allClocks = []
        if (Array.isArray(response.data)) {
          allClocks = response.data
        } else if (response.data.results) {
          allClocks = response.data.results
        } else if (response.data.attendances) {
          allClocks = response.data.attendances
        }
        
        // Filtrer pour aujourd'hui
        const today = new Date().toDateString()
        todayClocks.value = allClocks.filter(clock => {
          const clockDate = new Date(clock.timestamp || clock.clock_time || clock.date || clock.created_at).toDateString()
          return clockDate === today
        })
      } catch (error) {
        console.error('Erreur lors du chargement des pointages:', error)
        console.error('Détails:', error.response?.data)
      } finally {
        loadingClocks.value = false
      }
    }

    const formatTime = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
    }

    const isLate = (clock) => {
      const type = getClockType(clock)
      if (type !== 'in') return false
      const hour = new Date(clock.timestamp).getHours()
      return hour >= 9 // Considéré en retard après 9h
    }

    const getClockType = (clock) => {
      const type = clock.clock_type || clock.attendance_type || clock.type || ''
      return type.toLowerCase()
    }

    const getUserName = (clock) => {
      // Essayer différentes propriétés pour le nom
      if (clock.user_name) return clock.user_name
      if (clock.user && typeof clock.user === 'object') {
        return `${clock.user.first_name || ''} ${clock.user.last_name || ''}`.trim()
      }
      // Chercher dans les membres de l'équipe
      if (team.value && team.value.members) {
        const userId = clock.user_id || clock.user
        const member = team.value.members.find(m => m.id === userId)
        if (member) {
          return `${member.first_name || ''} ${member.last_name || ''}`.trim()
        }
      }
      return 'Inconnu'
    }

    const getStatus = (clock) => {
      const type = getClockType(clock)
      if (type === 'out') return 'Parti'
      return isLate(clock) ? 'En retard' : 'À l\'heure'
    }

    const getStatusClass = (clock) => {
      const type = getClockType(clock)
      if (type === 'out') return 'badge-info'
      return isLate(clock) ? 'badge-warning' : 'badge-success'
    }

    const handleLogout = async () => {
      await authService.logout()
      router.push('/login')
    }

    onMounted(() => {
      fetchTeam()
      fetchTodayClocks()
    })

    return {
      user,
      team,
      todayClocks,
      teamTodayClocks,
      loadingTeam,
      loadingClocks,
      presentToday,
      absentToday,
      lateToday,
      formatTime,
      getUserName,
      getClockType,
      getStatus,
      getStatusClass,
      handleLogout
    }
  }
}
</script>

<style scoped>
.manager-dashboard {
  min-height: 100vh;
  background-color: var(--gray-light);
}

.dashboard-header {
  background: var(--white);
  box-shadow: var(--shadow-sm);
  padding: var(--spacing-lg) var(--spacing-xl);
  margin-bottom: var(--spacing-lg);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content h1 {
  color: var(--primary-color);
  margin: 0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.user-name {
  font-weight: 600;
  color: var(--black);
}

.user-role {
  color: var(--gray-dark);
  font-size: 14px;
}

.dashboard-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 var(--spacing-xl) var(--spacing-xl);
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: var(--spacing-lg);
}

.team-overview,
.today-clocks,
.team-members {
  grid-column: 1 / -1;
}

.team-size {
  font-weight: 600;
  color: var(--primary-color);
  margin-top: var(--spacing-sm);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: var(--spacing-lg);
  margin-top: var(--spacing-md);
}

.stat-item {
  text-align: center;
  padding: var(--spacing-lg);
  background: var(--primary-light);
  border-radius: var(--radius-md);
}

.stat-value {
  display: block;
  font-size: 32px;
  font-weight: 700;
  color: var(--primary-color);
  margin-bottom: var(--spacing-sm);
}

.stat-label {
  display: block;
  color: var(--gray-dark);
  font-size: 14px;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: var(--spacing-md);
}

.data-table th,
.data-table td {
  padding: var(--spacing-sm) var(--spacing-md);
  text-align: left;
  border-bottom: 1px solid var(--gray-light);
}

.data-table th {
  background: var(--primary-light);
  color: var(--primary-dark);
  font-weight: 600;
}

.badge {
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 500;
}

.badge-success {
  background: var(--success);
  color: var(--white);
}

.badge-danger {
  background: var(--error);
  color: var(--white);
}

.badge-warning {
  background: var(--warning);
  color: var(--white);
}

.badge-info {
  background: var(--info);
  color: var(--white);
}

.members-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: var(--spacing-md);
  margin-top: var(--spacing-md);
}

.member-card {
  padding: var(--spacing-md);
  background: var(--primary-light);
  border-radius: var(--radius-md);
  border-left: 4px solid var(--primary-color);
}

.member-info h4 {
  margin: 0 0 var(--spacing-xs) 0;
  color: var(--black);
}

.member-info p {
  margin: var(--spacing-xs) 0;
  color: var(--gray-dark);
  font-size: 14px;
}

.member-email {
  font-size: 12px;
  color: var(--gray-medium);
}

.loading,
.no-data {
  text-align: center;
  padding: var(--spacing-xl);
  color: var(--gray-medium);
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: var(--spacing-md);
    text-align: center;
  }

  .dashboard-content {
    grid-template-columns: 1fr;
  }
}
</style>
