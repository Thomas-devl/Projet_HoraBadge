<template>
  <div class="dashboard employee-dashboard">
    <header class="dashboard-header">
      <div class="header-content">
        <div class="header-left">
          <div class="logo-header">
            <svg width="50" height="50" viewBox="0 0 60 60" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="30" cy="30" r="28" fill="#1E88E5"/>
              <path d="M30 15V30L40 35" stroke="white" stroke-width="3" stroke-linecap="round"/>
              <circle cx="30" cy="30" r="3" fill="white"/>
            </svg>
          </div>
          <div class="header-titles">
            <h1>Tableau de bord - Employé</h1>
            <p class="date-today">{{ formattedDate }}</p>
          </div>
        </div>
        <div class="user-info">
          <div class="user-details">
            <span class="user-name">{{ user.first_name }} {{ user.last_name }}</span>
            <span class="user-role">{{ user.function || 'Employé' }}</span>
          </div>
          <button @click="handleLogout" class="btn btn-secondary btn-small">
            Déconnexion
          </button>
        </div>
      </div>
    </header>

    <main class="dashboard-content">
      <!-- Section Badgeage rapide -->
      <section class="card quick-badge full-width">
        <h2>⏰ Pointage</h2>
        <div class="badge-status">
          <div class="status-indicator" :class="isClockedIn ? 'clocked-in' : 'clocked-out'">
            <span>{{ isClockedIn ? '✓ Pointé' : '✗ Non pointé' }}</span>
          </div>
        </div>
        <div class="badge-actions">
          <button @click="clockIn" class="btn btn-primary btn-large" :disabled="isClockedIn">
            🟢 Pointer l'arrivée
          </button>
          <button @click="clockOut" class="btn btn-danger btn-large" :disabled="!isClockedIn">
            🔴 Pointer le départ
          </button>
        </div>
        <div v-if="lastClock" class="last-clock-info">
          <p><strong>Dernier pointage :</strong> {{ formatDateTime(lastClock.timestamp) }}</p>
          <p><strong>Type :</strong> {{ lastClock.attendance_type === 'IN' ? '🟢 Arrivée' : '🔴 Départ' }}</p>
        </div>
      </section>

      <!-- Section Équipe et Manager -->
      <section class="card team-info">
        <h2>👥 Mon équipe</h2>
        <div v-if="loading" class="loading">Chargement...</div>
        <div v-else-if="teamData.length === 0" class="no-data">Pas d'équipe assignée</div>
        <div v-else>
          <div v-for="team in teamData" :key="team.id" class="team-card">
            <h3>{{ team.name }}</h3>
            <p v-if="team.description" class="team-description">{{ team.description }}</p>
            
            <div v-if="team.manager" class="manager-section">
              <p class="section-title">👔 Responsable</p>
              <div class="person-card">
                <div class="person-name">{{ team.manager.first_name }} {{ team.manager.last_name }}</div>
                <div class="person-detail">{{ team.manager.function }}</div>
                <div class="person-detail">{{ team.manager.email }}</div>
              </div>
            </div>
            
            <div v-if="team.members.length > 0" class="members-section">
              <p class="section-title">👨‍💼 Équipiers ({{ team.members.length }})</p>
              <div class="members-list">
                <div v-for="member in team.members" :key="member.id" class="member-item">
                  <span class="member-name">{{ member.first_name }} {{ member.last_name }}</span>
                  <span class="member-function">{{ member.function }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Section Anomalies -->
      <section class="card anomalies-section">
        <h2>⚠️ Anomalies détectées</h2>
        <div v-if="loadingAnomalies" class="loading">Analyse des anomalies...</div>
        <div v-else-if="!anomalies || anomalies.total_anomalies === 0" class="no-anomalies">
          ✓ Aucune anomalie détectée
        </div>
        <div v-else class="anomalies-list">
          <!-- Pointages sans paire -->
          <div v-if="anomalies.unpaired_checkins.length > 0" class="anomaly-group critical">
            <h4>🔴 Entrées sans sortie ({{ anomalies.unpaired_checkins.length }})</h4>
            <div v-for="(item, idx) in anomalies.unpaired_checkins" :key="'unpaired-' + idx" class="anomaly-item">
              <span class="anomaly-date">{{ formatDateOnly(item.date) }}</span>
              <span class="anomaly-time">{{ formatTimeOnly(item.timestamp) }}</span>
              <span class="anomaly-desc">{{ item.description }}</span>
            </div>
          </div>
          
          <!-- Horaires anormaux -->
          <div v-if="anomalies.abnormal_hours.length > 0" class="anomaly-group warning">
            <h4>🟡 Horaires anormaux ({{ anomalies.abnormal_hours.length }})</h4>
            <div v-for="(item, idx) in anomalies.abnormal_hours" :key="'abnormal-' + idx" class="anomaly-item">
              <span class="anomaly-date">{{ formatDateOnly(item.date) }}</span>
              <span class="anomaly-time">{{ formatTimeOnly(item.timestamp) }}</span>
              <span class="anomaly-desc">{{ item.description }}</span>
            </div>
          </div>
          
          <!-- Doublons -->
          <div v-if="anomalies.duplicate_checkins.length > 0" class="anomaly-group info">
            <h4>ℹ️ Pointages en doublon ({{ anomalies.duplicate_checkins.length }})</h4>
            <div v-for="(item, idx) in anomalies.duplicate_checkins" :key="'duplicate-' + idx" class="anomaly-item">
              <span class="anomaly-date">{{ formatDateOnly(item.date) }}</span>
              <span class="anomaly-desc">{{ item.description }}</span>
            </div>
          </div>
          
          <!-- Jours manquants -->
          <div v-if="anomalies.missing_days.length > 0" class="anomaly-group info">
            <h4>📅 Jours sans pointage ({{ anomalies.missing_days.length }})</h4>
            <div v-for="(item, idx) in anomalies.missing_days" :key="'missing-' + idx" class="anomaly-item">
              <span class="anomaly-date">{{ formatDateOnly(item.date) }}</span>
              <span class="anomaly-desc">{{ item.description }}</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Statistiques -->
      <section class="card stats">
        <h2>📊 Mes statistiques</h2>
        <div class="stats-grid">
          <div class="stat-item">
            <span class="stat-value">{{ totalHours }}</span>
            <span class="stat-label">Heures ce mois</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ workingDays }}</span>
            <span class="stat-label">Jours travaillés</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ averageHoursPerDay }}</span>
            <span class="stat-label">Moyenne/jour</span>
          </div>
        </div>
      </section>

      <!-- Calendrier du mois -->
      <section class="card my-clocks full-width">
        <h2>📅 Vue semaine</h2>
        <WeeklyCalendar />
      </section>

      <!-- Mes pointages du mois -->
      <section class="card my-clocks full-width">
        <h2>📋 Mes pointages ce mois-ci</h2>
        <div v-if="loadingClocks" class="loading">Chargement...</div>
        <div v-else-if="dailySessions.length === 0" class="no-data">
          Aucun pointage ce mois-ci
        </div>
        <div v-else class="clocks-container">
          <div class="clocks-summary">
            <span>Total : {{ dailySessions.length }} jours travaillés</span>
          </div>
          <table class="data-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Arrivée</th>
                <th>Départ</th>
                <th>Durée</th>
                <th>Statut</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="session in dailySessions" :key="session.date" :class="session.checkOut ? 'status-complete' : 'status-incomplete'">
                <td>{{ formatDateOnly(session.date) }}</td>
                <td>
                  <span v-if="session.checkIn" class="time-badge check-in">
                    {{ formatTimeOnly(session.checkIn.timestamp) }}
                  </span>
                  <span v-else class="time-badge missing">—</span>
                </td>
                <td>
                  <span v-if="session.checkOut" class="time-badge check-out">
                    {{ formatTimeOnly(session.checkOut.timestamp) }}
                  </span>
                  <span v-else class="time-badge missing">—</span>
                </td>
                <td>
                  <span v-if="session.checkIn && session.checkOut" class="duration-badge">
                    {{ calculateDuration(session.checkIn.timestamp, session.checkOut.timestamp) }}
                  </span>
                  <span v-else class="duration-badge incomplete">Incomplète</span>
                </td>
                <td>
                  <span v-if="session.checkIn && session.checkOut" class="badge status-validated">
                    ✓ Complète
                  </span>
                  <span v-else class="badge status-incomplete">
                    ⚠ Incomplète
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
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
import WeeklyCalendar from '@/components/WeeklyCalendar.vue'

export default {
  name: 'EmployeeDashboard',
  components: {
    WeeklyCalendar
  },
  setup() {
    const router = useRouter()
    const user = ref(authService.getCurrentUser() || {})
    const clocks = ref([])
    const teamData = ref([])
    const anomalies = ref(null)
    const loading = ref(true)
    const loadingClocks = ref(false)
    const loadingAnomalies = ref(false)
    const isClockedIn = ref(false)
    const lastClock = ref(null)

    const formattedDate = computed(() => {
      const date = new Date()
      return date.toLocaleDateString('fr-FR', { 
        weekday: 'long', 
        day: 'numeric', 
        month: 'long', 
        year: 'numeric' 
      })
    })

    const totalHours = computed(() => {
      let total = 0
      
      // Utiliser dailySessions pour calculer correctement les heures
      dailySessions.value.forEach(session => {
        if (session.checkIn && session.checkOut) {
          const checkInTime = new Date(session.checkIn.timestamp)
          const checkOutTime = new Date(session.checkOut.timestamp)
          const hours = (checkOutTime - checkInTime) / (1000 * 60 * 60)
          total += hours
        }
      })
      
      return Math.round(total * 10) / 10
    })

    const workingDays = computed(() => {
      // Compter seulement les jours avec au moins un pointage (checkIn OU checkOut)
      return dailySessions.value.filter(session => 
        session.checkIn || session.checkOut
      ).length
    })

    const averageHoursPerDay = computed(() => {
      if (workingDays.value === 0) return 0
      return Math.round((totalHours.value / workingDays.value) * 10) / 10
    })

    // Grouper les pointages par jour
    const dailySessions = computed(() => {
      const sessions = {}
      
      // D'abord, grouper par date
      clocks.value.forEach(clock => {
        if (!sessions[clock.date]) {
          sessions[clock.date] = { date: clock.date, checkIn: null, checkOut: null }
        }
        
        if (clock.attendance_type === 'IN') {
          sessions[clock.date].checkIn = clock
        } else if (clock.attendance_type === 'OUT') {
          sessions[clock.date].checkOut = clock
        }
      })
      
      // Convertir en tableau et trier par date décroissante
      return Object.values(sessions)
        .sort((a, b) => new Date(b.date) - new Date(a.date))
    })

    const fetchTeamInfo = async () => {
      try {
        const response = await api.get('/users/me/team-info/')
        teamData.value = response.data.teams || []
      } catch (error) {
        console.error('Erreur lors du chargement de l\'équipe:', error)
      }
    }

    const fetchClocks = async () => {
      loadingClocks.value = true
      try {
        // Récupérer les pointages du mois courant
        const response = await api.get('/attendance/')
        clocks.value = response.data.results || response.data
        
        if (clocks.value.length > 0) {
          lastClock.value = clocks.value[0]
          const today = new Date().toISOString().split('T')[0]
          const todayClocks = clocks.value.filter(c => c.date === today)
          
          const lastCheckIn = todayClocks.filter(c => c.attendance_type === 'IN').pop()
          const lastCheckOut = todayClocks.filter(c => c.attendance_type === 'OUT').pop()
          
          isClockedIn.value = !lastCheckOut || (lastCheckIn && new Date(lastCheckIn.timestamp) > new Date(lastCheckOut.timestamp))
        }
      } catch (error) {
        console.error('Erreur lors du chargement des pointages:', error)
      } finally {
        loadingClocks.value = false
      }
    }

    const fetchAnomalies = async () => {
      loadingAnomalies.value = true
      try {
        const response = await api.get('/attendance/anomalies/')
        anomalies.value = response.data
      } catch (error) {
        console.error('Erreur lors du chargement des anomalies:', error)
      } finally {
        loadingAnomalies.value = false
      }
    }

    const clockIn = async () => {
      try {
        await api.post('/attendance/check-in/')
        await fetchClocks()
        alert('✓ Arrivée pointée avec succès !')
      } catch (error) {
        console.error('Erreur lors du pointage:', error)
        const errorMsg = error.response?.data?.error || 'Erreur lors du pointage'
        alert('❌ ' + errorMsg)
      }
    }

    const clockOut = async () => {
      try {
        await api.post('/attendance/check-out/')
        await fetchClocks()
        alert('✓ Départ pointé avec succès !')
      } catch (error) {
        console.error('Erreur lors du pointage:', error)
        const errorMsg = error.response?.data?.error || 'Erreur lors du pointage'
        alert('❌ ' + errorMsg)
      }
    }

    const formatDateTime = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('fr-FR') + ' à ' + date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
    }

    const formatDateOnly = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('fr-FR', { weekday: 'short', day: '2-digit', month: 'short' })
    }

    const formatTimeOnly = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
    }

    const calculateDuration = (checkInTime, checkOutTime) => {
      const checkIn = new Date(checkInTime)
      const checkOut = new Date(checkOutTime)
      const diffMs = checkOut - checkIn
      const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
      const diffMinutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60))
      return `${diffHours}h${String(diffMinutes).padStart(2, '0')}m`
    }

    const getStatusLabel = (status) => {
      const labels = {
        'PENDING': '⏳ En attente',
        'APPROVED': '✓ Validé',
        'REJECTED': '✗ Rejeté'
      }
      return labels[status] || status
    }

    const handleLogout = async () => {
      await authService.logout()
      router.push('/login')
    }

    onMounted(async () => {
      await Promise.all([
        fetchTeamInfo(),
        fetchClocks(),
        fetchAnomalies()
      ])
      loading.value = false
    })

    return {
      user,
      clocks,
      dailySessions,
      teamData,
      anomalies,
      loading,
      loadingClocks,
      loadingAnomalies,
      isClockedIn,
      lastClock,
      formattedDate,
      totalHours,
      workingDays,
      averageHoursPerDay,
      clockIn,
      clockOut,
      calculateDuration,
      formatDateTime,
      formatDateOnly,
      formatTimeOnly,
      getStatusLabel,
      handleLogout
    }
  }
}
</script>

<style scoped>
:root {
  --primary-color: #3498db;
  --primary-light: #ecf0f1;
  --primary-dark: #2980b9;
  --success: #2ecc71;
  --error: #e74c3c;
  --warning: #f39c12;
  --info: #3498db;
  --gray-light: #f8f9fa;
  --gray-dark: #666;
  --black: #2c3e50;
  --white: #fff;
  --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.1);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.15);
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
}

.employee-dashboard {
  min-height: 100vh;
  background-color: var(--gray-light);
}

.dashboard-header {
  background: var(--white);
  box-shadow: var(--shadow-sm);
  padding: var(--spacing-lg) var(--spacing-xl);
  margin-bottom: var(--spacing-lg);
  border-bottom: 3px solid var(--primary-color);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--spacing-lg);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.logo-header {
  display: flex;
  align-items: center;
}

.logo-header svg {
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

.header-titles {
  display: flex;
  flex-direction: column;
}

.header-left h1 {
  color: var(--primary-color);
  margin: 0 0 var(--spacing-xs) 0;
  font-size: 28px;
}

.date-today {
  margin: 0;
  color: var(--gray-dark);
  font-size: 14px;
  text-transform: capitalize;
}

.user-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.user-details {
  display: flex;
  flex-direction: column;
  text-align: right;
}

.user-name {
  font-weight: 600;
  color: var(--black);
}

.user-role {
  color: var(--gray-dark);
  font-size: 12px;
}

.btn-small {
  padding: var(--spacing-sm) var(--spacing-md);
  font-size: 12px;
}

.dashboard-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 var(--spacing-xl) var(--spacing-xl);
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: var(--spacing-lg);
}

.full-width {
  grid-column: 1 / -1;
}

.card {
  background: var(--white);
  border-radius: var(--radius-md);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
  transition: box-shadow 0.3s ease;
}

.card:hover {
  box-shadow: var(--shadow-md);
}

.card h2 {
  margin: 0 0 var(--spacing-md) 0;
  color: var(--primary-color);
  font-size: 18px;
}

.card h3 {
  margin: 0 0 var(--spacing-sm) 0;
  color: var(--black);
  font-size: 16px;
}

.badge-status {
  display: flex;
  justify-content: center;
  margin-bottom: var(--spacing-lg);
}

.status-indicator {
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: var(--radius-md);
  font-weight: 600;
  font-size: 18px;
}

.status-indicator.clocked-in {
  background: #d5f4e6;
  color: var(--success);
}

.status-indicator.clocked-out {
  background: #fadbd8;
  color: var(--error);
}

.badge-actions {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
  margin: var(--spacing-lg) 0;
}

.btn-large {
  padding: var(--spacing-md) var(--spacing-lg);
  font-size: 16px;
  min-width: 180px;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-primary {
  background: var(--success);
  color: var(--white);
}

.btn-primary:hover:not(:disabled) {
  background: #27ae60;
}

.btn-danger {
  background: var(--error);
  color: var(--white);
}

.btn-danger:hover:not(:disabled) {
  background: #c0392b;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.last-clock-info {
  margin-top: var(--spacing-md);
  padding: var(--spacing-md);
  background: var(--primary-light);
  border-radius: var(--radius-md);
  border-left: 4px solid var(--primary-color);
}

.last-clock-info p {
  margin: var(--spacing-xs) 0;
  color: var(--black);
}

.team-card {
  padding: var(--spacing-md);
  background: var(--gray-light);
  border-radius: var(--radius-md);
  margin-bottom: var(--spacing-md);
}

.team-description {
  margin: var(--spacing-sm) 0 var(--spacing-md) 0;
  color: var(--gray-dark);
  font-size: 13px;
  font-style: italic;
}

.section-title {
  margin: var(--spacing-md) 0 var(--spacing-sm) 0;
  font-size: 13px;
  font-weight: 600;
  color: var(--primary-color);
}

.manager-section {
  margin: var(--spacing-md) 0;
}

.person-card {
  padding: var(--spacing-sm) var(--spacing-md);
  background: var(--white);
  border-radius: var(--radius-sm);
  border-left: 3px solid var(--primary-color);
}

.person-name {
  font-weight: 600;
  color: var(--black);
  display: block;
}

.person-detail {
  font-size: 12px;
  color: var(--gray-dark);
  display: block;
}

.members-section {
  margin: var(--spacing-md) 0 0 0;
}

.members-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.member-item {
  padding: var(--spacing-sm) var(--spacing-md);
  background: var(--white);
  border-radius: var(--radius-sm);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.member-name {
  font-weight: 500;
  color: var(--black);
}

.member-function {
  font-size: 12px;
  color: var(--gray-dark);
}

/* Anomalies Section */
.anomalies-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.anomaly-group {
  border-radius: var(--radius-md);
  padding: var(--spacing-md);
}

.anomaly-group h4 {
  margin: 0 0 var(--spacing-sm) 0;
  font-size: 14px;
}

.anomaly-group.critical {
  background: #fdeaea;
  border-left: 4px solid var(--error);
}

.anomaly-group.critical h4 {
  color: var(--error);
}

.anomaly-group.warning {
  background: #fff3cd;
  border-left: 4px solid var(--warning);
}

.anomaly-group.warning h4 {
  color: var(--warning);
}

.anomaly-group.info {
  background: #d1ecf1;
  border-left: 4px solid var(--info);
}

.anomaly-group.info h4 {
  color: var(--info);
}

.anomaly-item {
  padding: var(--spacing-sm);
  background: var(--white);
  border-radius: var(--radius-sm);
  display: flex;
  gap: var(--spacing-md);
  align-items: center;
  font-size: 13px;
}

.anomaly-date {
  font-weight: 600;
  min-width: 80px;
}

.anomaly-time {
  color: var(--gray-dark);
  min-width: 50px;
}

.anomaly-desc {
  flex: 1;
}

.no-anomalies {
  text-align: center;
  padding: var(--spacing-lg);
  color: var(--success);
  font-size: 16px;
  font-weight: 600;
}

/* Stats */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: var(--spacing-md);
}

.stat-item {
  text-align: center;
  padding: var(--spacing-md);
  background: var(--primary-light);
  border-radius: var(--radius-md);
  border-top: 3px solid var(--primary-color);
}

.stat-value {
  display: block;
  font-size: 24px;
  font-weight: 700;
  color: var(--primary-color);
  margin-bottom: var(--spacing-xs);
}

.stat-label {
  display: block;
  color: var(--gray-dark);
  font-size: 12px;
}

/* Table */
.clocks-container {
  max-height: 500px;
  overflow-y: auto;
}

.clocks-summary {
  padding: var(--spacing-sm) var(--spacing-md);
  background: var(--gray-light);
  border-radius: var(--radius-sm);
  margin-bottom: var(--spacing-md);
  font-size: 13px;
  color: var(--gray-dark);
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  padding: var(--spacing-sm) var(--spacing-md);
  text-align: left;
  border-bottom: 1px solid #ddd;
  font-size: 13px;
}

.data-table th {
  background: var(--primary-light);
  color: var(--primary-dark);
  font-weight: 600;
  position: sticky;
  top: 0;
}

.data-table tbody tr:hover {
  background: var(--gray-light);
}

.badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 500;
}

.badge-success {
  background: #d5f4e6;
  color: var(--success);
}

.badge-danger {
  background: #fadbd8;
  color: var(--error);
}

.badge.status-pending {
  background: #fff3cd;
  color: var(--warning);
}

.badge.status-approved {
  background: #d5f4e6;
  color: var(--success);
}

.badge.status-rejected {
  background: #fadbd8;
  color: var(--error);
}

.loading,
.no-data {
  text-align: center;
  padding: var(--spacing-lg);
  color: var(--gray-dark);
}

/* Daily Sessions Styling */
.time-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
  font-family: 'Courier New', monospace;
}

.time-badge.check-in {
  background: #d5f4e6;
  color: var(--success);
}

.time-badge.check-out {
  background: #dfe6e9;
  color: #2d3436;
}

.time-badge.missing {
  background: #fadbd8;
  color: var(--error);
}

.duration-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  background: #ecf0f1;
  color: var(--black);
  font-family: 'Courier New', monospace;
}

.duration-badge.incomplete {
  background: #fff3cd;
  color: var(--warning);
}

.data-table tbody tr.status-complete {
  background: #f0fff4;
}

.data-table tbody tr.status-incomplete {
  background: #fffbf0;
}

.badge.status-validated {
  background: #d5f4e6;
  color: var(--success);
}

.badge.status-incomplete {
  background: #fff3cd;
  color: var(--warning);
}

/* Responsive */
@media (max-width: 1024px) {
  .dashboard-content {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    text-align: center;
  }

  .user-info {
    flex-direction: column;
    width: 100%;
  }

  .user-details {
    text-align: center;
  }

  .badge-actions {
    flex-direction: column;
  }

  .btn-large {
    width: 100%;
    min-width: unset;
  }

  .anomaly-item {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
