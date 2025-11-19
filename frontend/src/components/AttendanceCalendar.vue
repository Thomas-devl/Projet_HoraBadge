<template>
  <div class="attendance-calendar">
    <!-- En-tête avec navigation mois -->
    <div class="calendar-header">
      <button @click="previousMonth" class="btn-nav">← Mois précédent</button>
      <h3>{{ monthName }} {{ year }}</h3>
      <button @click="nextMonth" class="btn-nav">Mois suivant →</button>
    </div>

    <!-- Statistiques du mois -->
    <div class="month-stats">
      <div class="stat-box">
        <span class="stat-value">{{ stats.total_hours }}h</span>
        <span class="stat-label">Heures travaillées</span>
      </div>
      <div class="stat-box complete">
        <span class="stat-value">{{ stats.complete_days }}</span>
        <span class="stat-label">Jours complets</span>
      </div>
      <div class="stat-box incomplete">
        <span class="stat-value">{{ stats.incomplete_days }}</span>
        <span class="stat-label">Jours incomplets</span>
      </div>
      <div class="stat-box missing">
        <span class="stat-value">{{ stats.missing_days }}</span>
        <span class="stat-label">Jours manquants</span>
      </div>
    </div>

    <!-- Calendrier -->
    <div class="calendar-container">
      <!-- Jours de la semaine -->
      <div class="calendar-weekdays">
        <div class="weekday" v-for="day in weekDays" :key="day">{{ day }}</div>
      </div>

      <!-- Jours du mois -->
      <div class="calendar-grid">
        <div
          v-for="(week, weekIndex) in calendar"
          :key="weekIndex"
          class="calendar-week"
        >
          <div
            v-for="(day, dayIndex) in week"
            :key="dayIndex"
            class="calendar-day"
            :class="getDayClasses(day)"
          >
            <div v-if="day" class="day-content">
              <div class="day-number">{{ day.day }}</div>
              
              <div v-if="day.status === 'complete'" class="day-info complete">
                <div class="time-badge check-in">
                  ↓ {{ formatTime(day.check_in) }}
                </div>
                <div class="time-badge check-out">
                  ↑ {{ formatTime(day.check_out) }}
                </div>
                <div class="hours-badge">{{ formatHours(day.hours) }}</div>
              </div>

              <div v-else-if="day.status === 'incomplete'" class="day-info incomplete">
                <div v-if="day.check_in" class="time-badge check-in">
                  ↓ {{ formatTime(day.check_in) }}
                </div>
                <div v-if="day.check_out" class="time-badge check-out">
                  ↑ {{ formatTime(day.check_out) }}
                </div>
                <div v-if="!day.check_in && !day.check_out" class="status-badge">
                  Incomplet
                </div>
              </div>

              <div v-else-if="day.status === 'missing'" class="day-info missing">
                <span class="status-badge">Manquant</span>
              </div>

              <div v-else-if="day.status === 'empty'" class="day-info empty">
                <span class="status-badge">W-E</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Légende -->
    <div class="calendar-legend">
      <div class="legend-item">
        <div class="legend-color complete"></div>
        <span>Jour complet</span>
      </div>
      <div class="legend-item">
        <div class="legend-color incomplete"></div>
        <span>Jour incomplet</span>
      </div>
      <div class="legend-item">
        <div class="legend-color missing"></div>
        <span>Jour manquant</span>
      </div>
      <div class="legend-item">
        <div class="legend-color weekend"></div>
        <span>Week-end</span>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'

export default {
  name: 'AttendanceCalendar',
  setup() {
    const year = ref(new Date().getFullYear())
    const month = ref(new Date().getMonth() + 1)
    const calendar = ref([])
    const stats = ref({
      total_hours: 0,
      complete_days: 0,
      incomplete_days: 0,
      missing_days: 0
    })
    const loading = ref(false)

    const weekDays = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']

    const monthName = computed(() => {
      const months = [
        'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
        'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
      ]
      return months[month.value - 1]
    })

    const fetchCalendar = async () => {
      loading.value = true
      try {
        const response = await api.get(`/attendance/calendar/?year=${year.value}&month=${month.value}`)
        calendar.value = response.data.calendar || []
        stats.value = response.data.statistics || {}
      } catch (error) {
        console.error('Erreur lors du chargement du calendrier:', error)
      } finally {
        loading.value = false
      }
    }

    const previousMonth = () => {
      if (month.value === 1) {
        month.value = 12
        year.value--
      } else {
        month.value--
      }
      fetchCalendar()
    }

    const nextMonth = () => {
      if (month.value === 12) {
        month.value = 1
        year.value++
      } else {
        month.value++
      }
      fetchCalendar()
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
      return `${wholeHours}h${String(minutes).padStart(2, '0')}m`
    }

    const getDayClasses = (day) => {
      if (!day) return ''
      
      const classes = ['day-' + day.status]
      
      if (day.is_weekend) classes.push('weekend')
      if (day.is_today) classes.push('today')
      
      return classes.join(' ')
    }

    onMounted(() => {
      fetchCalendar()
    })

    return {
      year,
      month,
      calendar,
      stats,
      loading,
      monthName,
      weekDays,
      previousMonth,
      nextMonth,
      formatTime,
      formatHours,
      getDayClasses
    }
  }
}
</script>

<style scoped>
.attendance-calendar {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* En-tête */
.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 2px solid #ecf0f1;
}

.calendar-header h3 {
  margin: 0;
  font-size: 20px;
  color: #2c3e50;
  min-width: 200px;
  text-align: center;
}

.btn-nav {
  background: #3498db;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  transition: background 0.3s ease;
}

.btn-nav:hover {
  background: #2980b9;
}

/* Statistiques du mois */
.month-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 12px;
  margin-bottom: 24px;
}

.stat-box {
  padding: 16px;
  border-radius: 8px;
  background: #ecf0f1;
  text-align: center;
  border-left: 4px solid #3498db;
}

.stat-box.complete {
  border-left-color: #2ecc71;
}

.stat-box.incomplete {
  border-left-color: #f39c12;
}

.stat-box.missing {
  border-left-color: #e74c3c;
}

.stat-value {
  display: block;
  font-size: 24px;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 4px;
}

.stat-label {
  display: block;
  font-size: 12px;
  color: #666;
}

/* Calendrier */
.calendar-container {
  margin-bottom: 24px;
}

.calendar-weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
  margin-bottom: 8px;
}

.weekday {
  text-align: center;
  font-weight: 600;
  font-size: 12px;
  color: #3498db;
  padding: 8px;
  background: #ecf0f1;
  border-radius: 4px;
}

.calendar-grid {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.calendar-week {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
}

.calendar-day {
  min-height: 100px;
  border: 2px solid #ddd;
  border-radius: 8px;
  padding: 8px;
  background: white;
  transition: all 0.3s ease;
  position: relative;
}

.calendar-day:not(.empty):hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.calendar-day.day-complete {
  background: #d5f4e6;
  border-color: #2ecc71;
}

.calendar-day.day-incomplete {
  background: #fff3cd;
  border-color: #f39c12;
}

.calendar-day.day-missing {
  background: #fdeaea;
  border-color: #e74c3c;
}

.calendar-day.day-empty {
  background: #f8f9fa;
  border-color: #e0e0e0;
}

.calendar-day.weekend {
  background: #f8f9fa;
  opacity: 0.8;
}

.calendar-day.today {
  border-width: 3px;
  box-shadow: inset 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.day-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
  height: 100%;
}

.day-number {
  font-weight: 700;
  font-size: 14px;
  color: #2c3e50;
}

.day-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
  font-size: 11px;
}

.time-badge {
  padding: 3px 6px;
  border-radius: 3px;
  color: white;
  text-align: center;
  font-weight: 600;
}

.time-badge.check-in {
  background: #2ecc71;
}

.time-badge.check-out {
  background: #3498db;
}

.hours-badge {
  background: #9b59b6;
  color: white;
  padding: 3px 6px;
  border-radius: 3px;
  text-align: center;
  font-weight: 600;
}

.status-badge {
  padding: 3px 6px;
  border-radius: 3px;
  text-align: center;
  font-weight: 600;
  background: rgba(0, 0, 0, 0.1);
}

/* Légende */
.calendar-legend {
  display: flex;
  gap: 24px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  flex-wrap: wrap;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: 3px;
  border: 2px solid #ddd;
}

.legend-color.complete {
  background: #d5f4e6;
  border-color: #2ecc71;
}

.legend-color.incomplete {
  background: #fff3cd;
  border-color: #f39c12;
}

.legend-color.missing {
  background: #fdeaea;
  border-color: #e74c3c;
}

.legend-color.weekend {
  background: #f8f9fa;
  border-color: #bbb;
}

/* Responsive */
@media (max-width: 768px) {
  .attendance-calendar {
    padding: 16px;
  }

  .calendar-header {
    flex-direction: column;
    gap: 12px;
  }

  .calendar-day {
    min-height: 80px;
    padding: 6px;
    font-size: 12px;
  }

  .day-number {
    font-size: 12px;
  }

  .time-badge,
  .hours-badge {
    font-size: 10px;
  }

  .calendar-legend {
    flex-direction: column;
    gap: 12px;
  }
}
</style>
