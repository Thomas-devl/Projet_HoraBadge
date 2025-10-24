<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-card card">
        <!-- Logo et Titre -->
        <div class="login-header">
          <div class="logo-container">
            <img src="@/assets/images/logo.svg" alt="HoraBadge Logo" class="logo" v-if="false" />
            <div class="logo-placeholder">
              <svg width="60" height="60" viewBox="0 0 60 60" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="30" cy="30" r="28" fill="#1E88E5"/>
                <path d="M30 15V30L40 35" stroke="white" stroke-width="3" stroke-linecap="round"/>
                <circle cx="30" cy="30" r="3" fill="white"/>
              </svg>
            </div>
          </div>
          <h1 class="login-title">HoraBadge</h1>
          <p class="login-subtitle">Connectez-vous à votre espace</p>
        </div>

        <!-- Messages d'erreur/succès -->
        <div v-if="errorMessage" class="alert alert-error">
          {{ errorMessage }}
        </div>
        <div v-if="successMessage" class="alert alert-success">
          {{ successMessage }}
        </div>

        <!-- Formulaire de connexion -->
        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label for="username" class="form-label">
              Nom d'utilisateur ou Email
            </label>
            <input
              id="username"
              v-model="loginForm.username"
              type="text"
              class="form-input"
              :class="{ error: errors.username }"
              placeholder="Entrez votre identifiant"
              autocomplete="username"
              required
            />
            <span v-if="errors.username" class="error-message">
              {{ errors.username }}
            </span>
          </div>

          <div class="form-group">
            <label for="password" class="form-label">
              Mot de passe
            </label>
            <div class="password-input-wrapper">
              <input
                id="password"
                v-model="loginForm.password"
                :type="showPassword ? 'text' : 'password'"
                class="form-input"
                :class="{ error: errors.password }"
                placeholder="Entrez votre mot de passe"
                autocomplete="current-password"
                required
              />
              <button
                type="button"
                class="password-toggle"
                @click="showPassword = !showPassword"
                tabindex="-1"
              >
                <span v-if="showPassword">👁️</span>
                <span v-else>👁️‍🗨️</span>
              </button>
            </div>
            <span v-if="errors.password" class="error-message">
              {{ errors.password }}
            </span>
          </div>

          <div class="form-options">
            <label class="checkbox-label">
              <input type="checkbox" v-model="rememberMe" />
              <span>Se souvenir de moi</span>
            </label>
            <a href="#" @click.prevent="showForgotPassword = true" class="forgot-password-link">
              Mot de passe oublié ?
            </a>
          </div>

          <button
            type="submit"
            class="btn btn-primary btn-full"
            :disabled="loading"
          >
            <span v-if="!loading">Se connecter</span>
            <span v-else class="loading-spinner">Connexion...</span>
          </button>
        </form>

        <!-- Lien vers l'inscription -->
        <div class="login-footer">
          <p class="text-muted">
            Vous n'avez pas de compte ?
            <a href="#" @click.prevent="handleRegisterRedirect">S'inscrire</a>
          </p>
        </div>
      </div>

      <!-- Modal Mot de passe oublié -->
      <div v-if="showForgotPassword" class="modal-overlay" @click="showForgotPassword = false">
        <div class="modal-content card" @click.stop>
          <h3 class="mb-md">Réinitialiser le mot de passe</h3>
          <p class="text-muted mb-lg">
            Entrez votre adresse email pour recevoir un lien de réinitialisation.
          </p>
          <form @submit.prevent="handlePasswordReset">
            <div class="form-group">
              <label for="reset-email" class="form-label">Email</label>
              <input
                id="reset-email"
                v-model="resetEmail"
                type="email"
                class="form-input"
                placeholder="votre@email.com"
                required
              />
            </div>
            <div class="modal-actions">
              <button type="button" class="btn btn-secondary" @click="showForgotPassword = false">
                Annuler
              </button>
              <button type="submit" class="btn btn-primary" :disabled="loading">
                Envoyer
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import authService from '@/services/authService'

export default {
  name: 'LoginPage',
  setup() {
    const router = useRouter()
    
    // État du formulaire
    const loginForm = reactive({
      username: '',
      password: ''
    })
    
    const errors = reactive({
      username: '',
      password: ''
    })
    
    const errorMessage = ref('')
    const successMessage = ref('')
    const loading = ref(false)
    const showPassword = ref(false)
    const rememberMe = ref(false)
    const showForgotPassword = ref(false)
    const resetEmail = ref('')
    
    // Validation du formulaire
    const validateForm = () => {
      let isValid = true
      errors.username = ''
      errors.password = ''
      
      if (!loginForm.username.trim()) {
        errors.username = 'Le nom d\'utilisateur est requis'
        isValid = false
      }
      
      if (!loginForm.password) {
        errors.password = 'Le mot de passe est requis'
        isValid = false
      } else if (loginForm.password.length < 6) {
        errors.password = 'Le mot de passe doit contenir au moins 6 caractères'
        isValid = false
      }
      
      return isValid
    }
    
    // Gérer la connexion
    const handleLogin = async () => {
      errorMessage.value = ''
      successMessage.value = ''
      
      if (!validateForm()) {
        return
      }
      
      loading.value = true
      
      try {
        const response = await authService.login(
          loginForm.username,
          loginForm.password
        )
        
        successMessage.value = 'Connexion réussie ! Redirection...'
        
        // Rediriger vers le dashboard après un court délai
        setTimeout(() => {
          router.push('/dashboard')
        }, 1000)
        
      } catch (error) {
        console.error('Erreur de connexion:', error)
        
        if (error.response) {
          // Erreur de l'API
          if (error.response.status === 401) {
            errorMessage.value = 'Identifiants incorrects. Veuillez réessayer.'
          } else if (error.response.data && error.response.data.detail) {
            errorMessage.value = error.response.data.detail
          } else {
            errorMessage.value = 'Une erreur est survenue lors de la connexion.'
          }
        } else if (error.request) {
          // Pas de réponse du serveur
          errorMessage.value = 'Impossible de contacter le serveur. Vérifiez votre connexion.'
        } else {
          // Autre erreur
          errorMessage.value = 'Une erreur inattendue est survenue.'
        }
      } finally {
        loading.value = false
      }
    }
    
    // Gérer la réinitialisation du mot de passe
    const handlePasswordReset = async () => {
      if (!resetEmail.value) {
        return
      }
      
      loading.value = true
      errorMessage.value = ''
      
      try {
        await authService.requestPasswordReset(resetEmail.value)
        successMessage.value = 'Un email de réinitialisation a été envoyé.'
        showForgotPassword.value = false
        resetEmail.value = ''
      } catch (error) {
        console.error('Erreur de réinitialisation:', error)
        errorMessage.value = 'Erreur lors de l\'envoi de l\'email.'
      } finally {
        loading.value = false
      }
    }
    
    // Redirection vers l'inscription
    const handleRegisterRedirect = () => {
      router.push('/register')
    }
    
    return {
      loginForm,
      errors,
      errorMessage,
      successMessage,
      loading,
      showPassword,
      rememberMe,
      showForgotPassword,
      resetEmail,
      handleLogin,
      handlePasswordReset,
      handleRegisterRedirect
    }
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--primary-light) 0%, var(--gray-light) 100%);
  padding: var(--spacing-lg);
}

.login-container {
  width: 100%;
  max-width: 440px;
}

.login-card {
  padding: var(--spacing-xl);
  background: var(--white);
  box-shadow: var(--shadow-lg);
}

.login-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.logo-container {
  margin-bottom: var(--spacing-md);
  display: flex;
  justify-content: center;
}

.logo {
  width: 60px;
  height: 60px;
}

.logo-placeholder {
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

.login-title {
  font-size: 2rem;
  color: var(--primary-color);
  margin-bottom: var(--spacing-sm);
}

.login-subtitle {
  color: var(--gray-dark);
  font-size: 1rem;
}

.alert {
  padding: var(--spacing-md);
  border-radius: var(--radius-md);
  margin-bottom: var(--spacing-md);
  font-size: 14px;
}

.alert-error {
  background-color: rgba(244, 67, 54, 0.1);
  color: var(--error);
  border: 1px solid var(--error);
}

.alert-success {
  background-color: rgba(76, 175, 80, 0.1);
  color: var(--success);
  border: 1px solid var(--success);
}

.login-form {
  margin-bottom: var(--spacing-lg);
}

.password-input-wrapper {
  position: relative;
}

.password-toggle {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  font-size: 20px;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.6;
  transition: opacity var(--transition-normal);
}

.password-toggle:hover {
  opacity: 1;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
  font-size: 14px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  cursor: pointer;
  color: var(--gray-dark);
}

.checkbox-label input[type="checkbox"] {
  cursor: pointer;
}

.forgot-password-link {
  font-size: 14px;
}

.loading-spinner {
  display: inline-block;
}

.login-footer {
  text-align: center;
  padding-top: var(--spacing-lg);
  border-top: 1px solid var(--gray-light);
}

/* Modal */
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
  width: 100%;
  max-width: 400px;
  padding: var(--spacing-xl);
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-actions {
  display: flex;
  gap: var(--spacing-md);
  justify-content: flex-end;
  margin-top: var(--spacing-lg);
}

/* Responsive */
@media (max-width: 768px) {
  .login-page {
    padding: var(--spacing-md);
  }
  
  .login-card {
    padding: var(--spacing-lg);
  }
  
  .login-title {
    font-size: 1.75rem;
  }
  
  .form-options {
    flex-direction: column;
    gap: var(--spacing-sm);
    align-items: flex-start;
  }
  
  .modal-actions {
    flex-direction: column;
  }
  
  .modal-actions .btn {
    width: 100%;
  }
}
</style>
