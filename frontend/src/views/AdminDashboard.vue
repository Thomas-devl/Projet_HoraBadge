<template>
  <div class="dashboard admin-dashboard">
    <header class="dashboard-header">
      <div class="header-content">
        <h1>Tableau de bord - Administrateur</h1>
        <div class="user-info">
          <span class="user-name">{{ user.full_name }}</span>
          <span class="user-role">Administrateur</span>
          <button @click="handleLogout" class="btn btn-secondary">
            Déconnexion
          </button>
        </div>
      </div>
    </header>

    <main class="dashboard-content">
      <!-- Statistiques globales -->
      <section class="card global-stats">
        <h2>Vue d'ensemble</h2>
        <div class="stats-grid">
          <div class="stat-item">
            <span class="stat-value">{{ totalUsers }}</span>
            <span class="stat-label">Total Utilisateurs</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ totalTeams }}</span>
            <span class="stat-label">Équipes</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ presentToday }}</span>
            <span class="stat-label">Présents aujourd'hui</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ totalClocksToday }}</span>
            <span class="stat-label">Pointages aujourd'hui</span>
          </div>
        </div>
      </section>

      <!-- Gestion des utilisateurs -->
      <section class="card users-section">
        <div class="section-header">
          <h2>Utilisateurs</h2>
          <button @click="editUser(null)" class="btn btn-primary">
            + Ajouter un utilisateur
          </button>
        </div>
        <div v-if="loadingUsers" class="loading">Chargement...</div>
        <table v-else class="data-table">
          <thead>
            <tr>
              <th>Nom</th>
              <th>Email</th>
              <th>Rôle</th>
              <th>Fonction</th>
              <th>Statut</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="usr in users" :key="usr.id">
              <td>{{ usr.full_name }}</td>
              <td>{{ usr.email }}</td>
              <td>
                <span :class="['badge', `badge-${usr.role}`]">
                  {{ getRoleLabel(usr.role) }}
                </span>
              </td>
              <td>{{ usr.function || '-' }}</td>
              <td>
                <span :class="['badge', usr.is_active ? 'badge-success' : 'badge-danger']">
                  {{ usr.is_active ? 'Actif' : 'Inactif' }}
                </span>
              </td>
              <td>
                <button @click="editUser(usr)" class="btn-icon" title="Modifier">
                  ✏️
                </button>
                <button @click="deleteUser(usr)" class="btn-icon" title="Supprimer">
                  🗑️
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </section>

      <!-- Gestion des équipes -->
      <section class="card teams-section">
        <div class="section-header">
          <h2>Équipes</h2>
          <button @click="editTeam(null)" class="btn btn-primary">
            + Créer une équipe
          </button>
        </div>
        <div v-if="loadingTeams" class="loading">Chargement...</div>
        <div v-else class="teams-grid">
          <div v-for="team in teams" :key="team.id" class="team-card card">
            <h3>{{ team.name }}</h3>
            <p>{{ team.description }}</p>
            <div class="team-info">
              <p><strong>Manager:</strong> {{ getManagerName(team.manager) }}</p>
              <p><strong>Membres:</strong> {{ team.members?.length || 0 }}</p>
            </div>
            <div class="team-actions">
              <button @click="editTeam(team)" class="btn btn-secondary btn-sm">
                Modifier
              </button>
              <button @click="deleteTeam(team)" class="btn btn-danger btn-sm">
                Supprimer
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- Accès rapides -->
      <section class="card quick-links">
        <h2>Accès rapides</h2>
        <div class="links-grid">
          <a href="/admin" target="_blank" class="quick-link">
            <span class="link-icon">⚙️</span>
            <span class="link-text">Admin Django</span>
          </a>
          <router-link to="/dashboard/employee" class="quick-link">
            <span class="link-icon">👤</span>
            <span class="link-text">Vue Employé</span>
          </router-link>
          <router-link to="/dashboard/manager" class="quick-link">
            <span class="link-icon">👔</span>
            <span class="link-text">Vue Manager</span>
          </router-link>
        </div>
      </section>
    </main>

    <!-- Modal utilisateur -->
    <div v-if="showUserModal" class="modal-overlay" @click="closeUserModal">
      <div class="modal-content card" @click.stop>
        <div class="modal-header">
          <h3>{{ editingUser ? 'Modifier' : 'Ajouter' }} un utilisateur</h3>
          <button @click="closeUserModal" class="btn-close">✕</button>
        </div>

        <form @submit.prevent="saveUser" class="user-form">
          <!-- Nom d'utilisateur -->
          <div class="form-group">
            <label for="username">Nom d'utilisateur *</label>
            <input
              id="username"
              v-model="userForm.username"
              type="text"
              required
              placeholder="john.doe"
              :disabled="!!editingUser"
            />
            <small v-if="!editingUser" class="form-hint">Unique, sans espaces</small>
          </div>

          <!-- Email -->
          <div class="form-group">
            <label for="email">Email *</label>
            <input
              id="email"
              v-model="userForm.email"
              type="email"
              required
              placeholder="john.doe@horabadge.com"
            />
          </div>

          <!-- Prénom -->
          <div class="form-group">
            <label for="first_name">Prénom *</label>
            <input
              id="first_name"
              v-model="userForm.first_name"
              type="text"
              required
              placeholder="John"
            />
          </div>

          <!-- Nom -->
          <div class="form-group">
            <label for="last_name">Nom *</label>
            <input
              id="last_name"
              v-model="userForm.last_name"
              type="text"
              required
              placeholder="Doe"
            />
          </div>

          <!-- Mot de passe (seulement pour création) -->
          <div v-if="!editingUser" class="form-group">
            <label for="password">Mot de passe *</label>
            <input
              id="password"
              v-model="userForm.password"
              type="password"
              :required="!editingUser"
              placeholder="••••••••"
            />
            <small class="form-hint">Minimum 8 caractères</small>
          </div>

          <!-- Confirmation mot de passe (seulement pour création) -->
          <div v-if="!editingUser" class="form-group">
            <label for="password_confirm">Confirmer le mot de passe *</label>
            <input
              id="password_confirm"
              v-model="userForm.password_confirm"
              type="password"
              :required="!editingUser"
              placeholder="••••••••"
            />
            <small v-if="userForm.password !== userForm.password_confirm && userForm.password_confirm" class="form-hint error-hint">
              ⚠️ Les mots de passe ne correspondent pas
            </small>
          </div>

          <!-- Rôle -->
          <div class="form-group">
            <label for="role">Rôle *</label>
            <select id="role" v-model="userForm.role" required>
              <option value="employee">Employé</option>
              <option value="manager">Manager</option>
              <option value="admin">Administrateur</option>
            </select>
          </div>

          <!-- Fonction -->
          <div class="form-group">
            <label for="function">Fonction</label>
            <input
              id="function"
              v-model="userForm.function"
              type="text"
              placeholder="Développeur, RH, etc."
            />
          </div>

          <!-- Statut -->
          <div class="form-group">
            <label class="checkbox-label">
              <input v-model="userForm.is_active" type="checkbox" />
              <span>Compte actif</span>
            </label>
          </div>

          <!-- Message d'erreur -->
          <div v-if="userFormError" class="alert alert-error">
            {{ userFormError }}
          </div>

          <!-- Boutons -->
          <div class="modal-actions">
            <button type="button" @click="closeUserModal" class="btn btn-secondary">
              Annuler
            </button>
            <button type="submit" class="btn btn-primary" :disabled="savingUser">
              {{ savingUser ? 'Enregistrement...' : (editingUser ? 'Modifier' : 'Créer') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal équipe -->
    <div v-if="showTeamModal" class="modal-overlay" @click="closeTeamModal">
      <div class="modal-content card" @click.stop>
        <div class="modal-header">
          <h3>{{ editingTeam ? 'Modifier' : 'Créer' }} une équipe</h3>
          <button @click="closeTeamModal" class="btn-close">✕</button>
        </div>

        <form @submit.prevent="saveTeam" class="team-form">
          <!-- Nom de l'équipe -->
          <div class="form-group">
            <label for="team_name">Nom de l'équipe *</label>
            <input
              id="team_name"
              v-model="teamForm.name"
              type="text"
              required
              placeholder="Équipe Développement"
            />
          </div>

          <!-- Description -->
          <div class="form-group">
            <label for="team_description">Description</label>
            <textarea
              id="team_description"
              v-model="teamForm.description"
              rows="3"
              placeholder="Description de l'équipe..."
            ></textarea>
          </div>

          <!-- Manager -->
          <div class="form-group">
            <label for="team_manager">Manager *</label>
            <select id="team_manager" v-model="teamForm.manager" required>
              <option value="">-- Sélectionner un manager --</option>
              <option 
                v-for="manager in availableManagers" 
                :key="manager.id" 
                :value="manager.id"
              >
                {{ manager.full_name }} ({{ manager.email }})
              </option>
            </select>
            <small class="form-hint">Seuls les utilisateurs avec le rôle "Manager" ou "Admin" apparaissent</small>
          </div>

          <!-- Membres de l'équipe -->
          <div class="form-group">
            <label for="team_members">Membres de l'équipe</label>
            <select id="team_members" v-model="teamForm.members" multiple size="6">
              <option 
                v-for="usr in users" 
                :key="usr.id" 
                :value="usr.id"
              >
                {{ usr.full_name }} - {{ getRoleLabel(usr.role) }}
              </option>
            </select>
            <small class="form-hint">Maintenez Ctrl/Cmd pour sélectionner plusieurs membres</small>
          </div>

          <!-- Message d'erreur -->
          <div v-if="teamFormError" class="alert alert-error">
            {{ teamFormError }}
          </div>

          <!-- Boutons -->
          <div class="modal-actions">
            <button type="button" @click="closeTeamModal" class="btn btn-secondary">
              Annuler
            </button>
            <button type="submit" class="btn btn-primary" :disabled="savingTeam">
              {{ savingTeam ? 'Enregistrement...' : (editingTeam ? 'Modifier' : 'Créer') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import authService from '@/services/authService'
import api from '@/services/api'

export default {
  name: 'AdminDashboard',
  setup() {
    const router = useRouter()
    const user = ref(authService.getCurrentUser() || {})
    const users = ref([])
    const teams = ref([])
    const todayClocks = ref([])
    const loadingUsers = ref(false)
    const loadingTeams = ref(false)
    const showUserModal = ref(false)
    const showTeamModal = ref(false)
    const editingUser = ref(null)
    const editingTeam = ref(null)

    // Formulaire utilisateur
    const userForm = ref({
      username: '',
      email: '',
      first_name: '',
      last_name: '',
      password: '',
      password_confirm: '',
      role: 'employee',
      function: '',
      is_active: true
    })
    const savingUser = ref(false)
    const userFormError = ref('')

    // Formulaire équipe
    const teamForm = ref({
      name: '',
      description: '',
      manager: '',
      members: []
    })
    const savingTeam = ref(false)
    const teamFormError = ref('')

    const totalUsers = computed(() => users.value.length)
    const totalTeams = computed(() => teams.value.length)
    const presentToday = computed(() => {
      const uniqueUsers = new Set(todayClocks.value.map(c => c.user_id))
      return uniqueUsers.size
    })
    const totalClocksToday = computed(() => todayClocks.value.length)

    // Computed pour les managers disponibles
    const availableManagers = computed(() => {
      return users.value.filter(u => u.role === 'manager' || u.role === 'admin')
    })

    const fetchUsers = async () => {
      loadingUsers.value = true
      try {
        const response = await api.get('/users/')
        users.value = response.data.results || response.data
      } catch (error) {
        console.error('Erreur lors du chargement des utilisateurs:', error)
      } finally {
        loadingUsers.value = false
      }
    }

    const fetchTeams = async () => {
      loadingTeams.value = true
      try {
        const response = await api.get('/teams/')
        teams.value = response.data.results || response.data
      } catch (error) {
        console.error('Erreur lors du chargement des équipes:', error)
      } finally {
        loadingTeams.value = false
      }
    }

    const fetchTodayClocks = async () => {
      try {
        const response = await api.get('/attendance/clocks/')
        const allClocks = response.data.results || response.data
        const today = new Date().toDateString()
        todayClocks.value = allClocks.filter(clock => {
          const clockDate = new Date(clock.timestamp).toDateString()
          return clockDate === today
        })
      } catch (error) {
        console.error('Erreur lors du chargement des pointages:', error)
      }
    }

    const getRoleLabel = (role) => {
      const labels = {
        employee: 'Employé',
        manager: 'Manager',
        admin: 'Admin'
      }
      return labels[role] || role
    }

    const getManagerName = (manager) => {
      if (!manager) return 'Non assigné'
      
      // Si manager est un objet avec full_name
      if (typeof manager === 'object' && manager.full_name) {
        return manager.full_name
      }
      
      // Si manager est un ID
      const managerId = typeof manager === 'object' ? manager.id : manager
      const managerUser = users.value.find(u => u.id === managerId)
      return managerUser ? managerUser.full_name : 'Inconnu'
    }

    const editUser = (usr) => {
      editingUser.value = usr
      
      if (usr) {
        // Mode édition : pré-remplir le formulaire
        userForm.value = {
          username: usr.username,
          email: usr.email,
          first_name: usr.first_name,
          last_name: usr.last_name,
          password: '',
          password_confirm: '',
          role: usr.role || 'employee',
          function: usr.function || '',
          is_active: usr.is_active !== false
        }
      } else {
        // Mode création : formulaire vide
        resetUserForm()
      }
      
      showUserModal.value = true
    }

    const resetUserForm = () => {
      userForm.value = {
        username: '',
        email: '',
        first_name: '',
        last_name: '',
        password: '',
        password_confirm: '',
        role: 'employee',
        function: '',
        is_active: true
      }
      userFormError.value = ''
    }

    const closeUserModal = () => {
      showUserModal.value = false
      editingUser.value = null
      resetUserForm()
    }

    const saveUser = async () => {
      savingUser.value = true
      userFormError.value = ''

      try {
        if (editingUser.value) {
          // Mode édition
          const updateData = { ...userForm.value }
          // Supprimer seulement les champs de mot de passe
          delete updateData.password
          delete updateData.password_confirm
          // Le username reste dans les données (même s'il ne sera pas modifié par le backend)
          
          await api.put(`/users/${editingUser.value.id}/`, updateData)
          alert('Utilisateur modifié avec succès !')
        } else {
          // Mode création
          await api.post('/users/', userForm.value)
          alert('Utilisateur créé avec succès !')
        }

        await fetchUsers()
        closeUserModal()
      } catch (error) {
        console.error('Erreur lors de la sauvegarde:', error)
        
        if (error.response?.data?.message) {
          userFormError.value = error.response.data.message
        } else if (error.response?.data) {
          const errors = Object.entries(error.response.data)
            .map(([field, messages]) => `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`)
            .join('\n')
          userFormError.value = errors
        } else {
          userFormError.value = 'Erreur lors de la sauvegarde. Veuillez réessayer.'
        }
      } finally {
        savingUser.value = false
      }
    }

    const deleteUser = async (usr) => {
      if (confirm(`Êtes-vous sûr de vouloir supprimer ${usr.full_name} ?`)) {
        try {
          await api.delete(`/users/${usr.id}/`)
          await fetchUsers()
          alert('Utilisateur supprimé')
        } catch (error) {
          console.error('Erreur lors de la suppression:', error)
          alert('Erreur lors de la suppression')
        }
      }
    }

    const editTeam = (team) => {
      editingTeam.value = team
      
      if (team) {
        // Mode édition : pré-remplir le formulaire
        teamForm.value = {
          name: team.name,
          description: team.description || '',
          manager: team.manager?.id || team.manager || '',
          members: team.members?.map(m => m.id || m) || []
        }
      } else {
        // Mode création : formulaire vide
        resetTeamForm()
      }
      
      showTeamModal.value = true
    }

    const resetTeamForm = () => {
      teamForm.value = {
        name: '',
        description: '',
        manager: '',
        members: []
      }
      teamFormError.value = ''
    }

    const closeTeamModal = () => {
      showTeamModal.value = false
      editingTeam.value = null
      resetTeamForm()
    }

    const saveTeam = async () => {
      savingTeam.value = true
      teamFormError.value = ''

      try {
        if (editingTeam.value) {
          // Mode édition
          await api.put(`/teams/${editingTeam.value.id}/`, teamForm.value)
          alert('Équipe modifiée avec succès !')
        } else {
          // Mode création
          await api.post('/teams/', teamForm.value)
          alert('Équipe créée avec succès !')
        }

        await fetchTeams()
        closeTeamModal()
      } catch (error) {
        console.error('Erreur lors de la sauvegarde:', error)
        
        if (error.response?.data?.message) {
          teamFormError.value = error.response.data.message
        } else if (error.response?.data) {
          const errors = Object.entries(error.response.data)
            .map(([field, messages]) => `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`)
            .join('\n')
          teamFormError.value = errors
        } else {
          teamFormError.value = 'Erreur lors de la sauvegarde. Veuillez réessayer.'
        }
      } finally {
        savingTeam.value = false
      }
    }

    const deleteTeam = async (team) => {
      if (confirm(`Êtes-vous sûr de vouloir supprimer l'équipe ${team.name} ?`)) {
        try {
          await api.delete(`/teams/${team.id}/`)
          await fetchTeams()
          alert('Équipe supprimée')
        } catch (error) {
          console.error('Erreur lors de la suppression:', error)
          alert('Erreur lors de la suppression')
        }
      }
    }

    const handleLogout = async () => {
      await authService.logout()
      router.push('/login')
    }

    onMounted(() => {
      fetchUsers()
      fetchTeams()
      fetchTodayClocks()
    })

    return {
      user,
      users,
      teams,
      todayClocks,
      loadingUsers,
      loadingTeams,
      totalUsers,
      totalTeams,
      presentToday,
      totalClocksToday,
      availableManagers,
      showUserModal,
      showTeamModal,
      editingUser,
      editingTeam,
      userForm,
      savingUser,
      userFormError,
      teamForm,
      savingTeam,
      teamFormError,
      getRoleLabel,
      getManagerName,
      editUser,
      deleteUser,
      editTeam,
      deleteTeam,
      saveUser,
      closeUserModal,
      saveTeam,
      closeTeamModal,
      handleLogout
    }
  }
}
</script>

<style scoped>
.admin-dashboard {
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
  max-width: 1600px;
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
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 var(--spacing-xl) var(--spacing-xl);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
}

.global-stats {
  background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
  color: var(--white);
}

.global-stats h2 {
  color: var(--white);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-lg);
  margin-top: var(--spacing-md);
}

.stat-item {
  text-align: center;
  padding: var(--spacing-lg);
  background: rgba(255, 255, 255, 0.1);
  border-radius: var(--radius-md);
  backdrop-filter: blur(10px);
}

.stat-value {
  display: block;
  font-size: 36px;
  font-weight: 700;
  color: var(--white);
  margin-bottom: var(--spacing-sm);
}

.stat-label {
  display: block;
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
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

.btn-icon {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 18px;
  padding: var(--spacing-xs);
  margin: 0 var(--spacing-xs);
  opacity: 0.6;
  transition: opacity var(--transition-normal);
}

.btn-icon:hover {
  opacity: 1;
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

.badge-employee {
  background: var(--info);
  color: var(--white);
}

.badge-manager {
  background: var(--warning);
  color: var(--white);
}

.badge-admin {
  background: var(--error);
  color: var(--white);
}

.btn-sm {
  padding: 6px 12px;
  font-size: 14px;
}

.teams-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--spacing-lg);
}

.team-card {
  padding: var(--spacing-lg);
}

.team-card h3 {
  margin: 0 0 var(--spacing-sm) 0;
  color: var(--primary-color);
}

.team-info {
  margin: var(--spacing-md) 0;
  padding: var(--spacing-md) 0;
  border-top: 1px solid var(--gray-light);
  border-bottom: 1px solid var(--gray-light);
}

.team-info p {
  margin: var(--spacing-xs) 0;
  font-size: 14px;
}

.team-actions {
  display: flex;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-md);
}

.links-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-md);
  margin-top: var(--spacing-md);
}

.quick-link {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-lg);
  background: var(--primary-light);
  border-radius: var(--radius-md);
  text-decoration: none;
  color: var(--primary-dark);
  transition: all var(--transition-normal);
}

.quick-link:hover {
  background: var(--primary-color);
  color: var(--white);
  transform: translateY(-2px);
}

.link-icon {
  font-size: 32px;
}

.link-text {
  font-weight: 500;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: var(--spacing-lg);
}

.modal-content {
  max-width: 600px;
  width: 100%;
  padding: var(--spacing-xl);
  max-height: 90vh;
  overflow-y: auto;
  overflow-x: hidden;
  /* Scrollbar personnalisée pour Webkit (Chrome, Safari, Edge) */
  scrollbar-width: thin;
  scrollbar-color: var(--primary-color) var(--gray-light);
}

/* Scrollbar pour Webkit */
.modal-content::-webkit-scrollbar {
  width: 8px;
}

.modal-content::-webkit-scrollbar-track {
  background: var(--gray-light);
  border-radius: 4px;
}

.modal-content::-webkit-scrollbar-thumb {
  background: var(--primary-color);
  border-radius: 4px;
}

.modal-content::-webkit-scrollbar-thumb:hover {
  background: var(--primary-dark);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
  padding-bottom: var(--spacing-md);
  border-bottom: 1px solid var(--gray-light);
}

.modal-header h3 {
  margin: 0;
  color: var(--primary-color);
}

.btn-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: var(--gray-medium);
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-sm);
  transition: all var(--transition-normal);
}

.btn-close:hover {
  background: var(--gray-light);
  color: var(--black);
}

.user-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.form-group label {
  font-weight: 500;
  color: var(--black);
  font-size: 14px;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: var(--spacing-sm) var(--spacing-md);
  border: 1px solid var(--gray-medium);
  border-radius: var(--radius-sm);
  font-size: 16px;
  font-family: inherit;
  transition: border-color var(--transition-normal);
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px var(--primary-light);
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.form-group select[multiple] {
  min-height: 150px;
  padding: var(--spacing-xs);
  /* Scrollbar pour select multiple */
  scrollbar-width: thin;
  scrollbar-color: var(--primary-color) var(--gray-light);
}

.form-group select[multiple]::-webkit-scrollbar {
  width: 8px;
}

.form-group select[multiple]::-webkit-scrollbar-track {
  background: var(--gray-light);
  border-radius: 4px;
}

.form-group select[multiple]::-webkit-scrollbar-thumb {
  background: var(--primary-color);
  border-radius: 4px;
}

.form-group select[multiple]::-webkit-scrollbar-thumb:hover {
  background: var(--primary-dark);
}

.form-group select[multiple] option {
  padding: var(--spacing-sm);
  border-radius: var(--radius-sm);
  margin: 2px 0;
}

.form-group select[multiple] option:checked {
  background: var(--primary-color);
  color: var(--white);
}

.form-group input:disabled {
  background-color: var(--gray-light);
  cursor: not-allowed;
  opacity: 0.6;
}

.form-hint {
  color: var(--gray-dark);
  font-size: 12px;
  font-style: italic;
}

.form-hint.error-hint {
  color: var(--error);
  font-weight: 500;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  cursor: pointer;
  user-select: none;
}

.checkbox-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.alert {
  padding: var(--spacing-md);
  border-radius: var(--radius-sm);
  margin-bottom: var(--spacing-md);
}

.alert-error {
  background: #fee;
  border: 1px solid var(--error);
  color: #c00;
  white-space: pre-line;
}

.modal-actions {
  display: flex;
  gap: var(--spacing-sm);
  justify-content: flex-end;
  margin-top: var(--spacing-lg);
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--gray-light);
}

.modal-actions .btn {
  min-width: 120px;
}

.loading {
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

  .section-header {
    flex-direction: column;
    gap: var(--spacing-md);
  }

  .section-header .btn {
    width: 100%;
  }
}
</style>
