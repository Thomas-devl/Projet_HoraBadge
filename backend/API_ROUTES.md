# ✅ API HoraBadge - Routes Créées et Fonctionnelles

## 🎉 Résumé de ce qui a été créé

Toutes les routes pour connecter le frontend au backend sont maintenant **créées et fonctionnelles** !

---

## 📁 Fichiers Créés

### **1. Serializers** (`apps/attendance/serializers.py`)
- ✅ `AttendanceSerializer` - Convertir pointages en JSON
- ✅ `AttendanceCreateSerializer` - Créer nouveaux pointages
- ✅ `WorkSessionSerializer` - Sessions de travail
- ✅ `NotificationSerializer` - Notifications
- ✅ `AttendanceSettingsSerializer` - Paramètres utilisateur

### **2. Views** (`apps/attendance/views.py`)
- ✅ 15+ vues API pour toutes les opérations CRUD
- ✅ Authentification requise sur toutes les routes
- ✅ Logique métier complète (validations, notifications, etc.)

### **3. URLs** (`apps/attendance/urls.py`)
- ✅ 14 routes organisées par ressource
- ✅ Routes RESTful standards
- ✅ Routes custom pour actions spécifiques

---

## 🌐 Routes Disponibles

Le serveur fonctionne sur : **http://localhost:8000**

### **📊 Pointages (Attendance)**

```
GET    /api/attendance/              # Liste tous les pointages
POST   /api/attendance/              # Créer un pointage

GET    /api/attendance/<id>/         # Détail d'un pointage
PUT    /api/attendance/<id>/         # Modifier (complet)
PATCH  /api/attendance/<id>/         # Modifier (partiel)
DELETE /api/attendance/<id>/         # Supprimer

GET    /api/attendance/today/        # Mes pointages du jour

POST   /api/attendance/check-in/     # Pointer entrée (rapide)
POST   /api/attendance/check-out/    # Pointer sortie (rapide)

GET    /api/attendance/stats/        # Statistiques personnelles
```

### **💼 Sessions de Travail**

```
GET    /api/attendance/sessions/     # Mes sessions (paires IN/OUT)
```

### **🔔 Notifications**

```
GET    /api/attendance/notifications/              # Liste notifications
GET    /api/attendance/notifications/<id>/         # Détail notification
POST   /api/attendance/notifications/<id>/mark-read/  # Marquer comme lu
POST   /api/attendance/notifications/mark-all-read/   # Tout marquer lu
GET    /api/attendance/notifications/unread-count/    # Nombre non lus
```

### **⚙️ Paramètres**

```
GET    /api/attendance/settings/     # Mes paramètres
PUT    /api/attendance/settings/     # Modifier paramètres
PATCH  /api/attendance/settings/     # Modifier paramètres (partiel)
```

---

## 🧪 Tester l'API Maintenant

### **Option 1 : Interface Graphique (Recommandé pour débuter)**

Le serveur est déjà lancé, ouvrez simplement :

```
http://localhost:8000/api/attendance/
```

**Vous verrez :**
- 📋 Interface DRF (Django REST Framework) avec boutons cliquables
- 🔐 Bouton "Log in" en haut à droite
- 📊 Données JSON formatées
- ➕ Formulaires pour POST/PUT/PATCH

---

### **Option 2 : Interface Admin**

```
http://localhost:8000/admin/
```

**Actions possibles :**
- ✅ Créer un superutilisateur : Voir ci-dessous
- ✅ Créer des utilisateurs test
- ✅ Créer des pointages manuellement
- ✅ Voir les notifications générées automatiquement

---

## 👤 Créer un Superutilisateur

**Dans un nouveau terminal :**

```bash
cd /home/keirs/epitech/Projet_HoraBadge/backend
source venv/bin/activate
python manage.py createsuperuser
```

**Il demandera :**
```
Username: admin
Email: admin@horabadge.com
Password: ********
Password (again): ********
```

**Ensuite :**
1. Aller sur http://localhost:8000/admin/
2. Connectez-vous avec `admin` / votre mot de passe
3. Vous pouvez créer des utilisateurs, pointages, etc.

---

## 🔐 Authentification

Toutes les routes nécessitent une authentification par **Token**.

### **Créer un Token (Via Django Shell)**

```bash
python manage.py shell
```

```python
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.get(username='admin')
token, created = Token.objects.get_or_create(user=user)
print(f"Token: {token.key}")
```

**Copier le token affiché !**

---

## 📱 Exemples depuis le Frontend (Vue.js)

### **Configuration de base**

```javascript
// src/services/api.js
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  }
})

// Intercepteur pour ajouter le token automatiquement
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Token ${token}`
  }
  return config
})

export default api
```

---

### **Exemple 1 : Pointer l'entrée**

```javascript
// src/services/attendance.js
import api from './api'

export const checkIn = async (notes = '') => {
  try {
    const response = await api.post('/attendance/check-in/', { notes })
    return response.data
  } catch (error) {
    console.error('Erreur check-in:', error.response?.data)
    throw error
  }
}

// Utilisation dans un composant Vue
import { checkIn } from '@/services/attendance'

const handleCheckIn = async () => {
  try {
    const attendance = await checkIn('Arrivée au bureau')
    console.log('Pointage créé:', attendance)
    // Afficher notification succès
  } catch (error) {
    // Afficher erreur
  }
}
```

---

### **Exemple 2 : Voir mes pointages du jour**

```javascript
export const getTodayAttendances = async () => {
  const response = await api.get('/attendance/today/')
  return response.data
}

// Dans un composant Vue
import { getTodayAttendances } from '@/services/attendance'
import { ref, onMounted } from 'vue'

const attendances = ref([])

onMounted(async () => {
  attendances.value = await getTodayAttendances()
})
```

---

### **Exemple 3 : Voir les notifications non lues**

```javascript
export const getUnreadCount = async () => {
  const response = await api.get('/attendance/notifications/unread-count/')
  return response.data.count
}

// Badge de notification
<template>
  <div class="notification-badge">
    <span>🔔</span>
    <span v-if="unreadCount > 0" class="badge">{{ unreadCount }}</span>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getUnreadCount } from '@/services/attendance'

const unreadCount = ref(0)

onMounted(async () => {
  unreadCount.value = await getUnreadCount()
})
</script>
```

---

### **Exemple 4 : Voir les statistiques**

```javascript
export const getStats = async () => {
  const response = await api.get('/attendance/stats/')
  return response.data
}

// Résultat attendu:
{
  "total_attendances": 45,
  "check_ins": 23,
  "check_outs": 22,
  "current_month": 15,
  "current_week": 8,
  "unread_notifications": 2,
  "active_sessions": 1
}
```

---

## 🧪 Tester avec cURL (Terminal)

### **1. Check-in rapide**

```bash
curl -X POST http://localhost:8000/api/attendance/check-in/ \
  -H "Authorization: Token VOTRE_TOKEN_ICI" \
  -H "Content-Type: application/json" \
  -d '{"notes": "Arrivée au bureau"}'
```

### **2. Check-out rapide**

```bash
curl -X POST http://localhost:8000/api/attendance/check-out/ \
  -H "Authorization: Token VOTRE_TOKEN_ICI" \
  -H "Content-Type: application/json" \
  -d '{"notes": "Départ pour déjeuner"}'
```

### **3. Voir mes pointages du jour**

```bash
curl http://localhost:8000/api/attendance/today/ \
  -H "Authorization: Token VOTRE_TOKEN_ICI"
```

### **4. Voir mes statistiques**

```bash
curl http://localhost:8000/api/attendance/stats/ \
  -H "Authorization: Token VOTRE_TOKEN_ICI"
```

### **5. Notifications non lues**

```bash
curl http://localhost:8000/api/attendance/notifications/unread-count/ \
  -H "Authorization: Token VOTRE_TOKEN_ICI"
```

---

## 🎯 Fonctionnalités Incluses

### **✅ Système de Pointage**
- Check-in / Check-out automatique
- Horodatage précis
- Notes optionnelles
- Validation (pas de doublon)

### **✅ Sessions de Travail**
- Calcul automatique des sessions (paires IN/OUT)
- Durée de travail
- Filtrage par date

### **✅ Notifications Automatiques**
- Alerte si pointage manquant
- Notification de rappel
- Compteur de notifications non lues
- Marquage lu/non lu

### **✅ Statistiques**
- Total des pointages
- Pointages par mois/semaine
- Sessions actives
- Notifications non lues

### **✅ Paramètres Personnalisés**
- Horaires de travail
- Activer/désactiver notifications
- Equipe associée

### **✅ Interface Admin**
- Badges colorés (IN/OUT/BREAK)
- Filtres avancés
- Actions groupées
- Gestion complète

---

## 📚 Documentation

Trois guides ont été créés :

1. **`ROUTES_GUIDE.md`** - Comprendre Django de A à Z (pour débutants)
2. **`DEMARRAGE_RAPIDE.md`** - Commencer rapidement
3. **`API_ROUTES.md`** - Ce fichier (résumé final)

---

## 🚀 Résumé : Que faire maintenant ?

### **Backend (Terminé ✅)**
1. ✅ Routes créées
2. ✅ Base de données migrée
3. ✅ Serveur lancé sur http://localhost:8000

### **Frontend (À faire 🔨)**
1. **Créer les services API** (voir exemples ci-dessus)
2. **Créer les composants Vue** :
   - Formulaire check-in/check-out
   - Liste des pointages
   - Badge notifications
   - Dashboard statistiques
3. **Gérer l'authentification** :
   - Stockage token dans localStorage
   - Intercepteur axios
   - Route de login

---

## 🆘 Support

Si vous avez des questions sur :
- **Les routes** → Voir `ROUTES_GUIDE.md`
- **Comment démarrer** → Voir `DEMARRAGE_RAPIDE.md`
- **Exemples frontend** → Voir ci-dessus (section Vue.js)
- **Problèmes d'authentification** → Créer un token (voir ci-dessus)

---

## ✨ Tout est Prêt !

Le backend est **complètement fonctionnel** ! Vous pouvez maintenant :

1. ✅ **Tester l'API** sur http://localhost:8000/api/attendance/
2. ✅ **Créer un superuser** : `python manage.py createsuperuser`
3. ✅ **Tester l'admin** : http://localhost:8000/admin/
4. ✅ **Développer le frontend Vue.js** avec les exemples fournis

**Serveur actif sur :** http://localhost:8000 🚀
