<template>
  <div class="dashboard employee-dashboard">
    <header class="dashboard-header">
      <div class="header-content">
        <h1>Tableau de bord - Employé</h1>
        <div class="user-info">
          <span class="user-name">{{ user.full_name }}</span>
          <span class="user-role">{{ user.function || 'Employé' }}</span>
          <button @click="handleLogout" class="btn btn-secondary">
            Déconnexion
          </button>
        </div>
      </div>
    </header>

    <main class="dashboard-content">
      <!-- Section Badgeage rapide -->
      <section class="card quick-badge">
        <h2>Badgeage</h2>
        <div class="badge-actions">
          <button @click="clockIn" class="btn btn-primary btn-large" :disabled="isClockedIn">
            🟢 Pointer l'arrivée
          </button>
          <button @click="clockOut" class="btn btn-danger btn-large" :disabled="!isClockedIn">
            🔴 Pointer le départ
          </button>
        </div>
        <div v-if="lastClock" class="last-clock-info">
          <p>Dernier pointage : {{ formatDate(lastClock.timestamp) }}</p>
          <p>Type : {{ lastClock.clock_type === 'in' ? 'Arrivée' : 'Départ' }}</p>
        </div>
      </section>

      <!-- Mes pointages du mois -->
      <section class="card my-clocks">
        <h2>Mes pointages ce mois-ci</h2>
        <div v-if="loading" class="loading">Chargement...</div>
        <div v-else-if="clocks.length === 0" class="no-data">
          Aucun pointage ce mois-ci
        </div>
        <table v-else class="data-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Heure</th>
              <th>Type</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="clock in clocks" :key="clock.id">
              <td>{{ formatDate(clock.timestamp) }}</td>
              <td>{{ formatTime(clock.timestamp) }}</td>
              <td>
                <span :class="['badge', clock.clock_type === 'in' ? 'badge-success' : 'badge-danger']">
                  {{ clock.clock_type === 'in' ? 'Arrivée' : 'Départ' }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </section>

      <!-- Statistiques -->
      <section class="card stats">
        <h2>Mes statistiques</h2>
        <div class="stats-grid">
          <div class="stat-item">
            <span class="stat-value">{{ totalHours }}h</span>
            <span class="stat-label">Heures ce mois</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ workingDays }}</span>
            <span class="stat-label">Jours travaillés</span>
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
  name: 'EmployeeDashboard',
  setup() {
    const router = useRouter()
    const user = ref(authService.getCurrentUser() || {})
    const clocks = ref([])
    const loading = ref(false)
    const isClockedIn = ref(false)
    const lastClock = ref(null)

    const totalHours = computed(() => {
      // Calcul simple des heures (à améliorer)
      return Math.floor(clocks.value.length * 4)
    })

    const workingDays = computed(() => {
      // Nombre de jours uniques
      const dates = new Set(clocks.value.map(c => formatDate(c.timestamp)))
      return dates.size
    })

    const fetchClocks = async () => {
      loading.value = true
      try {
        const response = await api.get(`/users/${user.value.id}/clocks`)
        clocks.value = response.data.results || response.data
        
        if (clocks.value.length > 0) {
          lastClock.value = clocks.value[0]
          isClockedIn.value = lastClock.value.clock_type === 'in'
        }
      } catch (error) {
        console.error('Erreur lors du chargement des pointages:', error)
      } finally {
        loading.value = false
      }
    }

    const clockIn = async () => {
      try {
        await api.post(`/users/${user.value.id}/clocks`, {
          clock_type: 'in'
        })
        await fetchClocks()
        alert('Arrivée pointée avec succès !')
      } catch (error) {
        console.error('Erreur lors du pointage:', error)
        alert('Erreur lors du pointage')
      }
    }

    const clockOut = async () => {
      try {
        await api.post(`/users/${user.value.id}/clocks`, {
          clock_type: 'out'
        })
        await fetchClocks()
        alert('Départ pointé avec succès !')
      } catch (error) {
        console.error('Erreur lors du pointage:', error)
        alert('Erreur lors du pointage')
      }
    }

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('fr-FR')
    }

    const formatTime = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
    }

    const handleLogout = async () => {
      await authService.logout()
      router.push('/login')
    }

    onMounted(() => {
      fetchClocks()
    })

    return {
      user,
      clocks,
      loading,
      isClockedIn,
      lastClock,
      totalHours,
      workingDays,
      clockIn,
      clockOut,
      formatDate,
      formatTime,
      handleLogout
    }
  }
}
</script>

<style scoped>
.employee-dashboard {
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
  max-width: 1200px;
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
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--spacing-xl) var(--spacing-xl);
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-lg);
}

.quick-badge {
  grid-column: 1 / -1;
  text-align: center;
}

.badge-actions {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
  margin: var(--spacing-lg) 0;
}

.btn-large {
  padding: var(--spacing-lg) var(--spacing-xl);
  font-size: 18px;
  min-width: 200px;
}

.last-clock-info {
  margin-top: var(--spacing-md);
  padding: var(--spacing-md);
  background: var(--primary-light);
  border-radius: var(--radius-md);
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

  .badge-actions {
    flex-direction: column;
  }

  .btn-large {
    width: 100%;
  }
}
</style>
