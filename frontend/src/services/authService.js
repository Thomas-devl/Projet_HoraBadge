import api from './api'

class AuthService {
  /**
   * Connecte un utilisateur
   * @param {string} username - Nom d'utilisateur ou email
   * @param {string} password - Mot de passe
   * @returns {Promise} Réponse de l'API
   */
  async login(username, password) {
    try {
      const response = await api.post('/auth/login/', {
        username,
        password
      })
      
      if (response.data.token) {
        // Stocker le token dans le localStorage
        localStorage.setItem('token', response.data.token)
        localStorage.setItem('user', JSON.stringify(response.data.user))
      }
      
      return response.data
    } catch (error) {
      throw error
    }
  }

  /**
   * Déconnecte l'utilisateur
   * @returns {Promise}
   */
  async logout() {
    try {
      await api.post('/auth/logout/')
    } catch (error) {
      console.error('Erreur lors de la déconnexion:', error)
    } finally {
      // Toujours supprimer les données locales
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  }

  /**
   * Récupère le token stocké
   * @returns {string|null}
   */
  getToken() {
    return localStorage.getItem('token')
  }

  /**
   * Récupère l'utilisateur connecté
   * @returns {Object|null}
   */
  getCurrentUser() {
    const userStr = localStorage.getItem('user')
    return userStr ? JSON.parse(userStr) : null
  }

  /**
   * Vérifie si l'utilisateur est connecté
   * @returns {boolean}
   */
  isAuthenticated() {
    return !!this.getToken()
  }

  /**
   * Demande de réinitialisation de mot de passe
   * @param {string} email
   * @returns {Promise}
   */
  async requestPasswordReset(email) {
    try {
      const response = await api.post('/auth/password-reset/', { email })
      return response.data
    } catch (error) {
      throw error
    }
  }

  /**
   * Confirme la réinitialisation du mot de passe
   * @param {string} token
   * @param {string} newPassword
   * @returns {Promise}
   */
  async confirmPasswordReset(token, newPassword) {
    try {
      const response = await api.post('/auth/password-reset-confirm/', {
        token,
        password: newPassword
      })
      return response.data
    } catch (error) {
      throw error
    }
  }

  /**
   * Inscription d'un nouvel utilisateur
   * @param {Object} userData - Données de l'utilisateur
   * @returns {Promise}
   */
  async register(userData) {
    try {
      const response = await api.post('/auth/register/', userData)
      
      if (response.data.token) {
        localStorage.setItem('token', response.data.token)
        localStorage.setItem('user', JSON.stringify(response.data.user))
      }
      
      return response.data
    } catch (error) {
      throw error
    }
  }
}

export default new AuthService()
