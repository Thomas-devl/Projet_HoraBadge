# Page de Login - HoraBadge

## 📋 Description

Page de connexion professionnelle créée selon la charte graphique HoraBadge. Cette page permet aux utilisateurs de se connecter à leur espace personnel.

## 🎨 Design

La page respecte la charte graphique définie dans `/docs/CHARTE_GRAPHIQUE.md` :

- **Couleurs** : Bleu principal (#1E88E5), blanc, gris
- **Typographie** : Roboto
- **Composants** : Cartes avec ombres, boutons arrondis, inputs stylisés
- **Animations** : Transitions fluides et feedback visuel

## ✨ Fonctionnalités

### Connexion
- Champ nom d'utilisateur/email
- Champ mot de passe avec affichage/masquage
- Option "Se souvenir de moi"
- Validation des champs en temps réel
- Messages d'erreur et de succès

### Sécurité
- Validation côté client
- Gestion des tokens JWT
- Protection contre les erreurs réseau
- Redirection automatique après connexion

### Réinitialisation du mot de passe
- Modal pour demander la réinitialisation
- Envoi d'email de réinitialisation
- Interface intuitive

## 📁 Fichiers créés

```
frontend/src/
├── assets/styles/
│   └── main.css                    # Styles globaux avec variables CSS
├── services/
│   └── authService.js              # Service d'authentification
├── views/
│   └── Login.vue                   # Page de login
└── router/
    └── index.js                    # Router avec guards d'authentification
```

## 🔧 Configuration

### Variables d'environnement

Assurez-vous que le fichier `.env` contient :

```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_API_TIMEOUT=10000
```

### Routes API nécessaires

Le backend doit exposer ces endpoints :

- `POST /api/auth/login/` - Connexion
- `POST /api/auth/logout/` - Déconnexion
- `POST /api/auth/password-reset/` - Demande de réinitialisation
- `POST /api/auth/password-reset-confirm/` - Confirmation de réinitialisation

## 🚀 Utilisation

### Accès à la page

```
http://localhost:5173/login
```

### Navigation Guards

Le router inclut des guards pour :
- Rediriger les utilisateurs connectés vers `/dashboard`
- Rediriger les utilisateurs non connectés vers `/login` si nécessaire

### Exemple de route protégée

```javascript
{
  path: '/dashboard',
  name: 'Dashboard',
  component: Dashboard,
  meta: { requiresAuth: true }  // Nécessite authentification
}
```

## 📱 Responsive

La page est entièrement responsive :
- **Desktop** : Layout optimisé avec grande carte centrale
- **Tablet** : Adaptation des espacements
- **Mobile** : Boutons pleine largeur, navigation simplifiée

## 🎯 Améliorations futures

- [ ] Ajouter l'authentification OAuth (Google, Microsoft)
- [ ] Implémenter la double authentification (2FA)
- [ ] Ajouter un captcha pour la sécurité
- [ ] Internationalisation (i18n)
- [ ] Mode sombre

## 🐛 Débogage

### Problèmes courants

1. **Erreur de connexion** : Vérifier que le backend est lancé
2. **CORS** : Vérifier la configuration CORS du backend
3. **Token non sauvegardé** : Vérifier le localStorage du navigateur

### Console de débogage

```javascript
// Vérifier le token
console.log(authService.getToken())

// Vérifier l'utilisateur
console.log(authService.getCurrentUser())

// Vérifier l'authentification
console.log(authService.isAuthenticated())
```

## 📚 Documentation

- [Charte Graphique](../../docs/CHARTE_GRAPHIQUE.md)
- [API Routes](../../backend/API_ROUTES.md)
- [Guide des Routes Frontend](./ROUTES_GUIDE.md)
