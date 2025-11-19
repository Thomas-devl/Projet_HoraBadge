<template>
  <div class="yearly-calendar">
    <!-- En-tête avec navigation année -->
    <div class="calendar-header">
      <button @click="previousYear" class="btn-nav">← Année précédente</button>
      <h3>{{ year }}</h3>
      <button @click="nextYear" class="btn-nav">Année suivante →</button>
    </div>

    <!-- Vue par semaines -->
    <div class="weeks-container">
      <div v-for="(week, weekIndex) in weeksData" :key="weekIndex" class="week-row">
        <!-- Numéro de semaine -->
        <div class="week-number">
          <span>S{{ week.weekNumber }}</span>
        </div>

        <!-- Jours de la semaine -->
        <div class="week-days">
          <div
            v-for="(day, dayIndex) in week.days"
            :key="dayIndex"
            class="day-cell"
            :class="getDayClasses(day)"
          >
            <div v-if="day" class="day-content">
              <!-- Numéro du jour -->
              <div class="day-number">{{ day.day }}</div>
              
              <!-- Mois (pour les premiers jours du mois) -->
              <div v-if="day.isFirstDayOfMonth" class="month-label">
                {{ getMonthShort(day.month) }}
              </div>

              <!-- Données de pointage -->
              <div v-if="day.hasData" class="day-data">
                <div class="time-in">↓ {{ formatTime(day.checkIn) }}</div>
                <div class="time-out">↑ {{ formatTime(day.checkOut) }}</div>
              </div>
              
              <!-- Statut -->
              <div v-if="day.status" :class="['status-badge', 'status-' + day.status]">
                {{ getStatusSymbol(day.status) }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Légende -->
    <div class="calendar-legend">
      <div class="legend-item">
        <span class="legend-box complete"></span>
        <span>Jour complet</span>
      </div>
      <div class="legend-item">
        <span class="legend-box incomplete"></span>
        <span>Jour incomplet</span>
      </div>
      <div class="legend-item">
        <span class="legend-box missing"></span>
        <span>Jour manquant</span>
      </div>
      <div class="legend-item">
        <span class="legend-box weekend"></span>
        <span>Week-end</span>
      </div>
    </div>

    <!-- Statistiques annuelles -->
    <div class="yearly-stats">
      <div class="stat-box">
        <span class="stat-value">{{ stats.totalHours }}h</span>
        <span class="stat-label">Heures travaillées</span>
      </div>
      <div class="stat-box complete">
        <span class="stat-value">{{ stats.completeDays }}</span>
        <span class="stat-label">Jours complets</span>
      </div>
      <div class="stat-box incomplete">
        <span class="stat-value">{{ stats.incompleteDays }}</span>
        <span class="stat-label">Jours incomplets</span>
      </div>
      <div class="stat-box missing">
        <span class="stat-value">{{ stats.missingDays }}</span>
        <span class="stat-label">Jours manquants</span>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'

export default {
  name: 'YearlyCalendar',
  setup() {
    const year = ref(new Date().getFullYear())
    const attendances = ref([])
    const loading = ref(false)

    const stats = computed(() => {
      let totalHours = 0
      let completeDays = 0
      let incompleteDays = 0
      let missingDays = 0

      attendances.value.forEach(att => {
        if (att.status === 'complete') {
          completeDays++
          totalHours += att.hours || 0
        } else if (att.status === 'incomplete') {
          incompleteDays++
        } else if (att.status === 'missing') {
          missingDays++
        }
      })

      return {
        totalHours: Math.round(totalHours),
        completeDays,
        incompleteDays,
        missingDays
      }
    })

    const weeksData = computed(() => {
      const weeks = []
      const firstDay = new Date(year.value, 0, 1)
      const lastDay = new Date(year.value, 11, 31)
      
      // Créer un map des attendances par date
      const attendanceByDate = {}
      attendances.value.forEach(att => {
        attendanceByDate[att.date] = att
      })

      // Trouver le lundi de la première semaine
      let currentDate = new Date(firstDay)
      currentDate.setDate(currentDate.getDate() - (currentDate.getDay() || 7) + 1)

      let weekNumber = 1
      while (currentDate <= lastDay) {
        const week = {
          weekNumber,
          days: []
        }

        // Ajouter 7 jours
        for (let i = 0; i < 7; i++) {
          const dateStr = currentDate.toISOString().split('T')[0]
          const dayOfWeek = currentDate.getDay()
          const dayOfMonth = currentDate.getDate()
          const monthIndex = currentDate.getMonth()
          const yearNum = currentDate.getFullYear()

          // Vérifions si le jour est dans l'année cible
          if (yearNum === year.value) {
            const att = attendanceByDate[dateStr]
            const isFirstDayOfMonth = dayOfMonth === 1

            week.days.push({
              day: dayOfMonth,
              date: dateStr,
              month: monthIndex,
              isFirstDayOfMonth,
              dayOfWeek,
              status: att ? att.status : (dayOfWeek === 0 || dayOfWeek === 6 ? 'empty' : 'missing'),
              checkIn: att ? att.check_in : null,
              checkOut: att ? att.check_out : null,
              hours: att ? att.hours : 0,
              hasData: !!(att && att.check_in && att.check_out)
            })
          }

          currentDate.setDate(currentDate.getDate() + 1)
        }

        if (week.days.length > 0) {
          weeks.push(week)
        }
        weekNumber++
      }

      return weeks
    })

    const fetchAttendances = async () => {
      loading.value = true
      try {
        const response = await api.get(`/attendance/`)
        attendances.value = response.data.results || response.data
      } catch (error) {
        console.error('Erreur lors du chargement des pointages:', error)
      } finally {
        loading.value = false
      }
    }

    const previousYear = () => {
      year.value--
      fetchAttendances()
    }

    const nextYear = () => {
      year.value++
      fetchAttendances()
    }

    const formatTime = (timestamp) => {
      if (!timestamp) return '-'
      const date = new Date(timestamp)
      return date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
    }

    const getMonthShort = (monthIndex) => {
      const months = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc']
      return months[monthIndex]
    }

    const getStatusSymbol = (status) => {
      const symbols = {
        'complete': '✓',
        'incomplete': '⚠',
        'missing': '✗',
        'empty': '-'
      }
      return symbols[status] || ''
    }

    const getDayClasses = (day) => {
      if (!day) return ''
      const classes = ['day-' + day.status]
      if (day.dayOfWeek === 0 || day.dayOfWeek === 6) classes.push('weekend')
      return classes.join(' ')
    }

    onMounted(() => {
      fetchAttendances()
    })

    return {
      year,
      weeksData,
      stats,
      loading,
      previousYear,
      nextYear,
      formatTime,
      getMonthShort,
      getStatusSymbol,
      getDayClasses
    }
  }
}
</script>

<style scoped>
.yearly-calendar {
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
  font-size: 28px;
  color: #2c3e50;
  min-width: 120px;
  text-align: center;
}

.btn-nav {
  background: #3498db;
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.3s ease;
}

.btn-nav:hover {
  background: #2980b9;
}

/* Conteneur des semaines */
.weeks-container {
  margin-bottom: 24px;
  max-height: 800px;
  overflow-y: auto;
}

.week-row {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
  padding: 8px;
  background: #f8f9fa;
  border-radius: 8px;
  align-items: flex-start;
}

.week-number {
  min-width: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: #3498db;
  font-size: 12px;
  background: white;
  border-radius: 6px;
  padding: 4px 8px;
}

.week-days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
  flex: 1;
}

/* Cellule du jour */
.day-cell {
  min-height: 70px;
  border: 2px solid #ddd;
  border-radius: 6px;
  padding: 4px;
  background: white;
  font-size: 11px;
  position: relative;
}

.day-cell.day-complete {
  background: #d5f4e6;
  border-color: #2ecc71;
}

.day-cell.day-incomplete {
  background: #fff3cd;
  border-color: #f39c12;
}

.day-cell.day-missing {
  background: #fdeaea;
  border-color: #e74c3c;
}

.day-cell.day-empty {
  background: #f8f9fa;
  border-color: #e0e0e0;
  opacity: 0.6;
}

.day-cell.weekend {
  opacity: 0.7;
}

.day-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
  height: 100%;
}

.day-number {
  font-weight: 700;
  color: #2c3e50;
  font-size: 12px;
}

.month-label {
  font-size: 9px;
  color: #3498db;
  font-weight: 600;
}

.day-data {
  display: flex;
  flex-direction: column;
  gap: 2px;
  font-size: 10px;
  font-family: 'Courier New', monospace;
  flex: 1;
}

.time-in {
  color: #2ecc71;
  font-weight: 600;
}

.time-out {
  color: #3498db;
  font-weight: 600;
}

.status-badge {
  text-align: center;
  font-weight: 700;
  padding: 2px;
  border-radius: 3px;
}

.status-complete {
  color: #2ecc71;
}

.status-incomplete {
  color: #f39c12;
}

.status-missing {
  color: #e74c3c;
}

.status-empty {
  color: #999;
}

/* Légende */
.calendar-legend {
  display: flex;
  gap: 20px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}

.legend-box {
  width: 20px;
  height: 20px;
  border-radius: 4px;
  border: 2px solid #ddd;
}

.legend-box.complete {
  background: #d5f4e6;
  border-color: #2ecc71;
}

.legend-box.incomplete {
  background: #fff3cd;
  border-color: #f39c12;
}

.legend-box.missing {
  background: #fdeaea;
  border-color: #e74c3c;
}

.legend-box.weekend {
  background: #f8f9fa;
  border-color: #bbb;
}

/* Statistiques annuelles */
.yearly-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 16px;
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

/* Responsive */
@media (max-width: 1200px) {
  .week-days {
    grid-template-columns: repeat(7, minmax(50px, 1fr));
  }

  .day-cell {
    min-height: 60px;
    font-size: 10px;
  }

  .day-number {
    font-size: 11px;
  }

  .time-in,
  .time-out {
    font-size: 9px;
  }
}

@media (max-width: 768px) {
  .yearly-calendar {
    padding: 16px;
  }

  .calendar-header {
    flex-direction: column;
    gap: 12px;
  }

  .weeks-container {
    max-height: 600px;
  }

  .week-row {
    flex-direction: column;
  }

  .week-days {
    grid-template-columns: repeat(7, 1fr);
    width: 100%;
  }

  .day-cell {
    min-height: 50px;
    font-size: 9px;
  }

  .calendar-legend {
    flex-direction: column;
    gap: 12px;
  }
}
</style>
