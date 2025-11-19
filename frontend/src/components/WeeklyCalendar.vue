<template>
  <div class="weekly-calendar">
    <!-- Navigation semaine -->
    <div class="week-navigation">
      <button @click="previousWeek" class="nav-button prev-button">
        ← Semaine précédente
      </button>
      
      <div class="week-display">
        <div class="logo-week">
          <svg width="40" height="40" viewBox="0 0 60 60" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="30" cy="30" r="28" fill="#1E88E5"/>
            <path d="M30 15V30L40 35" stroke="white" stroke-width="3" stroke-linecap="round"/>
            <circle cx="30" cy="30" r="3" fill="white"/>
          </svg>
        </div>
        <h3>Semaine {{ weekNumber }}</h3>
        <p class="date-range">{{ formatWeekRange() }}</p>
      </div>
      
      <button @click="nextWeek" class="nav-button next-button">
        Semaine suivante →
      </button>
    </div>

    <!-- Bouton retour aujourd'hui -->
    <div class="today-action" v-if="weekOffset !== 0">
      <button @click="goToCurrentWeek" class="today-button">
        📅 Revenir à la semaine actuelle
      </button>
    </div>

    <!-- Vue des 5 jours de la semaine -->
    <div class="week-grid">
      <div
        v-for="(day, index) in weekDays"
        :key="index"
        :class="['day-card', getDayClasses(day)]"
      >
        <!-- Jour et date -->
        <div class="day-header">
          <div class="day-name">{{ formatDayName(day.date) }}</div>
          <div class="day-date">{{ formatDate(day.date) }}</div>
          <span v-if="isToday(day.date)" class="today-badge">Aujourd'hui</span>
        </div>

        <!-- Contenu du jour -->
        <div class="day-content">
          <!-- Si données de pointage -->
          <div v-if="day.hasData" class="day-data">
            <div class="time-slot check-in">
              <span class="time-label">🟢 Arrivée</span>
              <span class="time-value">{{ formatTime(day.checkIn) }}</span>
            </div>

            <div class="time-slot check-out">
              <span class="time-label">🔴 Départ</span>
              <span class="time-value">{{ formatTime(day.checkOut) }}</span>
            </div>

            <div class="total-hours">
              <span class="hours-label">Total :</span>
              <span class="hours-value">{{ formatHours(day.hours) }}</span>
            </div>
          </div>

          <!-- Si pas de données -->
          <div v-else class="day-empty">
            <div class="empty-icon">🕐</div>
            <p class="empty-text">{{ getEmptyText(day) }}</p>
          </div>
        </div>

        <!-- Statut du jour -->
        <div v-if="day.status" :class="['day-status', 'status-' + day.status]">
          {{ getStatusText(day.status) }}
        </div>
      </div>
    </div>

    <!-- Statistiques de la semaine -->
    <div class="week-stats">
      <div class="stat-item">
        <span class="stat-icon">⏱️</span>
        <span class="stat-label">Total heures</span>
        <span class="stat-value">{{ stats.totalHours }}h</span>
      </div>

      <div class="stat-item">
        <span class="stat-icon">✓</span>
        <span class="stat-label">Jours complets</span>
        <span class="stat-value">{{ stats.completeDays }}/5</span>
      </div>

      <div class="stat-item">
        <span class="stat-icon">⚠️</span>
        <span class="stat-label">Jours incomplets</span>
        <span class="stat-value">{{ stats.incompleteDays }}</span>
      </div>

      <div class="stat-item">
        <span class="stat-icon">✗</span>
        <span class="stat-label">Jours manquants</span>
        <span class="stat-value">{{ stats.missingDays }}</span>
      </div>
    </div>

    <!-- Légende -->
    <div class="calendar-legend">
      <div class="legend-item">
        <span class="legend-color complete"></span>
        <span>Jour complet</span>
      </div>
      <div class="legend-item">
        <span class="legend-color incomplete"></span>
        <span>Jour incomplet</span>
      </div>
      <div class="legend-item">
        <span class="legend-color missing"></span>
        <span>Jour manquant</span>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'

export default {
  name: 'WeeklyCalendar',
  setup() {
    const attendances = ref([])
    const loading = ref(false)
    
    // Utiliser un offset pour naviguer entre les semaines (0 = semaine actuelle)
    const weekOffset = ref(0)

    // Grouper les pointages par date (IN/OUT)
    const dailySessions = computed(() => {
      const sessions = {}
      
      attendances.value.forEach(att => {
        const dateStr = att.date
        if (!sessions[dateStr]) {
          sessions[dateStr] = { date: dateStr, checkIn: null, checkOut: null }
        }
        
        if (att.attendance_type === 'IN') {
          sessions[dateStr].checkIn = att.timestamp
        } else if (att.attendance_type === 'OUT') {
          sessions[dateStr].checkOut = att.timestamp
        }
      })
      
      return sessions
    })

    // Calculer les jours de la semaine actuelle
    const weekDays = computed(() => {
      const days = []
      
      // Trouver le lundi de la semaine (avec offset)
      const today = new Date()
      const currentDay = today.getDay()
      const diff = currentDay === 0 ? -6 : 1 - currentDay
      const monday = new Date(today)
      monday.setDate(today.getDate() + diff + (weekOffset.value * 7))
      monday.setHours(0, 0, 0, 0)

      // Ajouter seulement les 5 jours de semaine (lundi à vendredi)
      for (let i = 0; i < 5; i++) {
        const currentDate = new Date(monday)
        currentDate.setDate(currentDate.getDate() + i)
        
        // Utiliser le format local au lieu de toISOString pour éviter les décalages UTC
        const year = currentDate.getFullYear()
        const month = String(currentDate.getMonth() + 1).padStart(2, '0')
        const day = String(currentDate.getDate()).padStart(2, '0')
        const dateStr = `${year}-${month}-${day}`
        
        const session = dailySessions.value[dateStr]
        const hasCheckIn = session && session.checkIn
        const hasCheckOut = session && session.checkOut
        const hasData = hasCheckIn && hasCheckOut
        
        // Calculer les heures travaillées
        let hours = 0
        if (hasData) {
          const checkInTime = new Date(session.checkIn)
          const checkOutTime = new Date(session.checkOut)
          hours = (checkOutTime - checkInTime) / (1000 * 60 * 60)
        }

        // Déterminer le statut
        let status = 'missing'
        if (hasData) {
          status = 'complete'
        } else if (hasCheckIn || hasCheckOut) {
          status = 'incomplete'
        }

        days.push({
          date: currentDate,
          dateStr,
          dayOfWeek: currentDate.getDay(),
          status,
          checkIn: session ? session.checkIn : null,
          checkOut: session ? session.checkOut : null,
          hours: Math.round(hours * 10) / 10,
          hasData
        })
      }

      return days
    })

    const stats = computed(() => {
      let totalHours = 0
      let completeDays = 0
      let incompleteDays = 0
      let missingDays = 0

      // Tous les jours de weekDays sont des jours de semaine (lundi-vendredi)
      weekDays.value.forEach(day => {
        if (day.status === 'complete') {
          completeDays++
          totalHours += day.hours || 0
        } else if (day.status === 'incomplete') {
          incompleteDays++
        } else if (day.status === 'missing') {
          missingDays++
        }
      })

      return {
        totalHours: Math.round(totalHours * 10) / 10,
        completeDays,
        incompleteDays,
        missingDays
      }
    })

    const fetchAttendances = async () => {
      loading.value = true
      try {
        const response = await api.get(`/attendance/`)
        attendances.value = response.data.results || response.data
        console.log('📊 Attendances reçues:', attendances.value)
        console.log('📅 Daily sessions groupées:', dailySessions.value)
      } catch (error) {
        console.error('Erreur lors du chargement des pointages:', error)
      } finally {
        loading.value = false
      }
    }

    const previousWeek = () => {
      console.log('🔙 Semaine précédente cliquée, offset avant:', weekOffset.value)
      weekOffset.value--
      console.log('🔙 Nouveau offset:', weekOffset.value)
    }

    const nextWeek = () => {
      console.log('🔜 Semaine suivante cliquée, offset avant:', weekOffset.value)
      weekOffset.value++
      console.log('🔜 Nouveau offset:', weekOffset.value)
    }
    
    const goToCurrentWeek = () => {
      console.log('📅 Retour à aujourd\'hui, offset avant:', weekOffset.value)
      weekOffset.value = 0
      console.log('📅 Nouveau offset:', weekOffset.value)
    }
    
    const weekNumber = computed(() => {
      if (weekDays.value.length === 0) return 1
      const firstDay = weekDays.value[0].date
      const firstDayOfYear = new Date(firstDay.getFullYear(), 0, 1)
      const pastDaysOfYear = (firstDay - firstDayOfYear) / 86400000
      return Math.ceil((pastDaysOfYear + firstDayOfYear.getDay() + 1) / 7)
    })

    const formatWeekRange = () => {
      if (weekDays.value.length === 0) return ''
      const firstDay = weekDays.value[0].date
      const lastDay = weekDays.value[4].date
      const options = { day: 'numeric', month: 'long', year: 'numeric' }
      return `${firstDay.toLocaleDateString('fr-FR', options)} - ${lastDay.toLocaleDateString('fr-FR', options)}`
    }

    const formatDayName = (date) => {
      return date.toLocaleDateString('fr-FR', { weekday: 'long' })
    }

    const formatDate = (date) => {
      return date.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short', year: 'numeric' })
    }

    const formatTime = (timestamp) => {
      if (!timestamp) return '-'
      const date = new Date(timestamp)
      return date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
    }

    const formatHours = (hours) => {
      if (!hours) return '0h'
      const wholeHours = Math.floor(hours)
      const minutes = Math.round((hours - wholeHours) * 60)
      if (minutes === 0) return `${wholeHours}h`
      return `${wholeHours}h ${String(minutes).padStart(2, '0')}m`
    }

    const isToday = (date) => {
      const now = new Date()
      return date.toDateString() === now.toDateString()
    }

    const getEmptyText = (day) => {
      if (day.dayOfWeek === 0 || day.dayOfWeek === 6) {
        return 'Week-end'
      }
      return 'Aucun pointage'
    }

    const getStatusText = (status) => {
      const texts = {
        'complete': '✓ Complet',
        'incomplete': '⚠ Incomplet',
        'missing': '✗ Manquant',
        'empty': 'W-E'
      }
      return texts[status] || ''
    }

    const getDayClasses = (day) => {
      const classes = ['day-' + day.status]
      if (day.dayOfWeek === 0 || day.dayOfWeek === 6) classes.push('weekend')
      if (isToday(day.date)) classes.push('today')
      return classes.join(' ')
    }

    onMounted(() => {
      fetchAttendances()
    })

    return {
      weekDays,
      weekNumber,
      weekOffset,
      stats,
      loading,
      previousWeek,
      nextWeek,
      goToCurrentWeek,
      formatWeekRange,
      formatDayName,
      formatDate,
      formatTime,
      formatHours,
      isToday,
      getEmptyText,
      getStatusText,
      getDayClasses
    }
  }
}
</script>

<style scoped>
:root {
  /* Couleurs Charte */
  --primary-blue: #1E88E5;
  --primary-blue-dark: #1565C0;
  --primary-blue-light: #E3F2FD;
  --white: #FFFFFF;
  --gray-light: #F5F5F5;
  --gray-medium: #9E9E9E;
  --gray-dark: #424242;
  --black: #212121;
  --success: #4CAF50;
  --error: #F44336;
  --warning: #FF9800;
  --info: #00BCD4;
}

.weekly-calendar {
  background: var(--white);
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* === EN-TÊTE NAVIGATION === */
.week-navigation {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
  padding: 20px;
  background: var(--primary-blue-light);
  border-radius: 12px;
}

.week-display {
  text-align: center;
  flex: 1;
}

.logo-week {
  display: flex;
  justify-content: center;
  margin-bottom: 8px;
}

.logo-week svg {
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

.week-display h3 {
  margin: 0 0 5px 0;
  font-size: 24px;
  font-weight: 700;
  color: var(--primary-blue);
}

.date-range {
  margin: 0;
  font-size: 14px;
  color: var(--gray-dark);
  font-weight: 500;
}

.nav-button {
  background: #1E88E5 !important;
  color: #FFFFFF !important;
  border: none;
  padding: 14px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 15px !important;
  font-weight: 600 !important;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  min-width: 180px;
  text-align: center;
}

.nav-button:hover {
  background: #1565C0 !important;
  color: #FFFFFF !important;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.nav-button:active {
  transform: translateY(0);
}

.today-action {
  text-align: center;
  margin-bottom: 20px;
}

.today-button {
  background: #00BCD4 !important;
  color: #FFFFFF !important;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px !important;
  font-weight: 500 !important;
  transition: all 0.3s ease;
}

.today-button:hover {
  background: #0097A7 !important;
  color: #FFFFFF !important;
  transform: scale(1.05);
}

/* === GRILLE DE JOURS === */
.week-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
  margin-bottom: 32px;
}

.day-card {
  border: 2px solid var(--gray-light);
  border-radius: 12px;
  padding: 16px;
  background: var(--white);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  min-height: 280px;
}

.day-card:hover:not(.day-empty) {
  box-shadow: 0 4px 16px rgba(30, 136, 229, 0.15);
  border-color: var(--primary-blue);
}

.day-card.day-complete {
  background: #F1F8F5;
  border-color: var(--success);
}

.day-card.day-incomplete {
  background: #FFFBF0;
  border-color: var(--warning);
}

.day-card.day-missing {
  background: #FEF5F5;
  border-color: var(--error);
}

.day-card.day-empty {
  background: var(--gray-light);
  border-color: var(--gray-medium);
  opacity: 0.7;
}

.day-card.today {
  border-width: 3px;
  box-shadow: 0 0 0 3px var(--primary-blue-light);
}

.day-card.weekend {
  opacity: 0.8;
}

/* === EN-TÊTE DU JOUR === */
.day-header {
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(30, 136, 229, 0.2);
}

.day-name {
  font-size: 16px;
  font-weight: 700;
  color: var(--primary-blue);
  text-transform: capitalize;
  margin-bottom: 4px;
}

.day-date {
  font-size: 12px;
  color: var(--gray-dark);
}

.today-badge {
  display: inline-block;
  background: var(--primary-blue);
  color: var(--white);
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 10px;
  font-weight: 600;
  margin-top: 8px;
}

/* === CONTENU DU JOUR === */
.day-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.day-data {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.time-slot {
  padding: 12px;
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.time-slot.check-in {
  background: rgba(76, 175, 80, 0.1);
  border-left: 4px solid var(--success);
}

.time-slot.check-out {
  background: rgba(0, 188, 212, 0.1);
  border-left: 4px solid var(--info);
}

.time-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--gray-dark);
}

.time-value {
  font-size: 14px;
  font-weight: 700;
  color: var(--primary-blue);
  font-family: 'Roboto Mono', monospace;
}

.total-hours {
  background: var(--primary-blue-light);
  padding: 12px;
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-left: 4px solid var(--primary-blue);
}

.hours-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--gray-dark);
}

.hours-value {
  font-size: 16px;
  font-weight: 700;
  color: var(--primary-blue);
  font-family: 'Roboto Mono', monospace;
}

/* === JOUR VIDE === */
.day-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  text-align: center;
  flex: 1;
}

.empty-icon {
  font-size: 40px;
  opacity: 0.4;
}

.empty-text {
  margin: 0;
  font-size: 13px;
  color: var(--gray-dark);
}

/* === STATUT DU JOUR === */
.day-status {
  text-align: center;
  font-size: 12px;
  font-weight: 600;
  padding: 8px;
  border-radius: 6px;
  margin-top: 12px;
}

.day-status.status-complete {
  background: rgba(76, 175, 80, 0.1);
  color: var(--success);
}

.day-status.status-incomplete {
  background: rgba(255, 152, 0, 0.1);
  color: var(--warning);
}

.day-status.status-missing {
  background: rgba(244, 67, 54, 0.1);
  color: var(--error);
}

.day-status.status-empty {
  background: transparent;
  color: var(--gray-dark);
}

/* === STATISTIQUES === */
.week-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 16px;
  margin-bottom: 32px;
  padding: 24px;
  background: var(--gray-light);
  border-radius: 12px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  text-align: center;
}

.stat-icon {
  font-size: 24px;
}

.stat-label {
  font-size: 12px;
  color: var(--gray-dark);
  font-weight: 500;
}

.stat-value {
  font-size: 20px;
  font-weight: 700;
  color: var(--primary-blue);
  font-family: 'Roboto Mono', monospace;
}

/* === LÉGENDE === */
.calendar-legend {
  display: flex;
  gap: 24px;
  padding: 16px 24px;
  background: var(--primary-blue-light);
  border-radius: 12px;
  flex-wrap: wrap;
  justify-content: center;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--gray-dark);
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: 4px;
  border: 2px solid var(--gray-medium);
}

.legend-color.complete {
  background: #F1F8F5;
  border-color: var(--success);
}

.legend-color.incomplete {
  background: #FFFBF0;
  border-color: var(--warning);
}

.legend-color.missing {
  background: #FEF5F5;
  border-color: var(--error);
}

.legend-color.weekend {
  background: var(--gray-light);
  border-color: var(--gray-medium);
}

/* === RESPONSIVE === */
@media (max-width: 1024px) {
  .weekly-calendar {
    padding: 24px;
  }

  .week-grid {
    grid-template-columns: repeat(5, 1fr);
  }

  .day-card {
    min-height: 250px;
  }
}

@media (max-width: 768px) {
  .weekly-calendar {
    padding: 16px;
  }

  .calendar-header {
    flex-direction: column;
    gap: 16px;
    margin-bottom: 24px;
    padding-bottom: 16px;
  }

  .week-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    margin-bottom: 24px;
  }

  .day-card {
    min-height: 220px;
    padding: 12px;
  }

  .day-name {
    font-size: 14px;
  }

  .day-date {
    font-size: 11px;
  }

  .time-value {
    font-size: 13px;
  }

  .hours-value {
    font-size: 14px;
  }

  .week-stats {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    padding: 16px;
  }

  .calendar-legend {
    flex-direction: column;
    gap: 12px;
  }
}

@media (max-width: 480px) {
  .weekly-calendar {
    padding: 12px;
  }

  .week-grid {
    grid-template-columns: 1fr;
  }

  .day-card {
    min-height: 200px;
  }

  .btn-nav {
    padding: 10px 16px;
    font-size: 12px;
  }

  .week-info h3 {
    font-size: 20px;
  }
}
</style>
