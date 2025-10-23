# 🚀 Guide de Démarrage Rapide

## ✅ État Actuel du Projet

### **Ce qui est fait :**
- ✅ Django REST Framework installé
- ✅ Base de données configurée (SQLite pour dev)
- ✅ Migrations créées et appliquées
- ✅ 15+ routes API créées
- ✅ Système de notifications prêt
- ✅ Interface admin configurée

---

## 📝 Prochaines Étapes

### **1️⃣ Créer un Superutilisateur (Admin)**

```bash
cd /home/keirs/epitech/Projet_HoraBadge/backend
source venv/bin/activate
python manage.py createsuperuser
```

**Il vous demandera :**
- Username : `admin` (par exemple)
- Email : `admin@horabadge.com`
- Password : (choisissez un mot de passe)

---

### **2️⃣ Démarrer le Serveur**

```bash
python manage.py runserver
```

**Résultat :**
```
Starting development server at http://127.0.0.1:8000/
```

---

### **3️⃣ Tester l'Interface Admin**

**URL :** http://localhost:8000/admin/

**Connexion :**
- Username : `admin`
- Password : (celui que vous avez choisi)

**Vous pouvez :**
- ✅ Créer des utilisateurs
- ✅ Créer des équipes
- ✅ Créer des pointages manuellement
- ✅ Voir les notifications
- ✅ Gérer les paramètres

---

### **4️⃣ Tester les Routes API**

#### **a) Interface Graphique (DRF Browsable API)**

Ouvrez dans le navigateur :
```
http://localhost:8000/api/attendance/
```

**Vous verrez :**
- 📋 Interface graphique pour tester l'API
- 🔐 Formulaire de connexion en haut à droite
- 📊 Données au format JSON
- ➕ Formulaires pour créer/modifier

---

#### **b) Test avec cURL (Terminal)**

```bash
# 1. Créer un utilisateur test
curl -X POST http://localhost:8000/api/attendance/check-in/ \
  -H "Content-Type: application/json" \
  -d '{"notes": "Test de pointage"}'
```

**⚠️ Note :** Sans authentification, vous aurez l'erreur :
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

### **5️⃣ Créer un Token d'Authentification**

#### **Option A : Via Django Shell**

```bash
python manage.py shell
```

```python
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.get(username='admin')
token, created = Token.objects.get_or_create(user=user)
print(f"Token : {token.key}")
```

**Résultat :**
```
Token : 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

#### **Option B : Via l'Admin**

1. Aller sur http://localhost:8000/admin/
2. Cliquer sur **Tokens** (ajouté automatiquement par DRF)
3. Créer un nouveau token

---

### **6️⃣ Tester avec Authentification**

```bash
# Remplacer YOUR_TOKEN par le token généré
curl -X POST http://localhost:8000/api/attendance/check-in/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{"notes": "Arrivée au bureau"}'
```

**Résultat attendu :**
```json
{
  "id": 1,
  "user": 1,
  "user_username": "admin",
  "attendance_type": "IN",
  "timestamp": "2025-01-23T08:30:00Z",
  "date": "2025-01-23",
  "notes": "Arrivée au bureau"
}
```

---

## 📋 Liste des Routes Disponibles

### **Pointages (Attendance)**

| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/api/attendance/` | Liste tous les pointages |
| POST | `/api/attendance/` | Créer un pointage |
| GET | `/api/attendance/1/` | Détail du pointage #1 |
| PUT | `/api/attendance/1/` | Modifier complet |
| PATCH | `/api/attendance/1/` | Modifier partiel |
| DELETE | `/api/attendance/1/` | Supprimer |
| GET | `/api/attendance/today/` | Mes pointages du jour |
| POST | `/api/attendance/check-in/` | Pointer entrée rapide |
| POST | `/api/attendance/check-out/` | Pointer sortie rapide |
| GET | `/api/attendance/stats/` | Statistiques |

### **Sessions de Travail**

| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/api/attendance/sessions/` | Liste des sessions |

### **Notifications**

| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/api/attendance/notifications/` | Mes notifications |
| GET | `/api/attendance/notifications/1/` | Détail notification |
| POST | `/api/attendance/notifications/1/mark-read/` | Marquer comme lu |
| POST | `/api/attendance/notifications/mark-all-read/` | Tout marquer lu |
| GET | `/api/attendance/notifications/unread-count/` | Nombre non lus |

### **Paramètres**

| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/api/attendance/settings/` | Mes paramètres |
| PUT | `/api/attendance/settings/` | Modifier paramètres |

---

## 🧪 Exemples de Requêtes

### **1. Créer un pointage d'entrée**

```bash
curl -X POST http://localhost:8000/api/attendance/check-in/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "notes": "Arrivée au bureau"
  }'
```

### **2. Créer un pointage de sortie**

```bash
curl -X POST http://localhost:8000/api/attendance/check-out/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "notes": "Départ pour déjeuner"
  }'
```

### **3. Voir mes pointages du jour**

```bash
curl http://localhost:8000/api/attendance/today/ \
  -H "Authorization: Token YOUR_TOKEN"
```

### **4. Voir mes statistiques**

```bash
curl http://localhost:8000/api/attendance/stats/ \
  -H "Authorization: Token YOUR_TOKEN"
```

### **5. Voir mes notifications non lues**

```bash
curl http://localhost:8000/api/attendance/notifications/unread-count/ \
  -H "Authorization: Token YOUR_TOKEN"
```

---

## 🔧 Commandes Utiles

### **Vérifier la configuration**
```bash
python manage.py check
```

### **Créer des migrations (après changement de modèle)**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **Lancer le serveur**
```bash
python manage.py runserver
```

### **Ouvrir le shell Django**
```bash
python manage.py shell
```

### **Vérifier les pointages manquants (cron job)**
```bash
python manage.py check_missing_attendance
```

### **Créer un superutilisateur**
```bash
python manage.py createsuperuser
```

---

## 🌐 Frontend (Vue.js)

### **Exemple de requête depuis Vue.js**

```javascript
// services/api.js
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  }
})

// Ajouter le token automatiquement
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Token ${token}`
  }
  return config
})

// Exemple d'utilisation
export const checkIn = (notes) => {
  return api.post('/attendance/check-in/', { notes })
}

export const getMyAttendances = () => {
  return api.get('/attendance/today/')
}

export const getStats = () => {
  return api.get('/attendance/stats/')
}
```

---

## 📖 Documentation Complète

Pour comprendre en détail comment fonctionnent les routes, consultez :
```
/backend/ROUTES_GUIDE.md
```

---

## 🎯 Résumé des Actions

1. ✅ **Créer superutilisateur** : `python manage.py createsuperuser`
2. ✅ **Lancer serveur** : `python manage.py runserver`
3. ✅ **Tester admin** : http://localhost:8000/admin/
4. ✅ **Tester API** : http://localhost:8000/api/attendance/
5. ✅ **Créer token** : Via shell ou admin
6. ✅ **Tester requêtes** : Avec cURL ou interface graphique

---

## 🚨 En Cas de Problème

### **Erreur : "No module named 'rest_framework'"**
```bash
pip install djangorestframework
```

### **Erreur : "CSRF verification failed"**
Dans les settings development, ajouter :
```python
CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'http://127.0.0.1:8000']
```

### **Erreur : "Authentication credentials were not provided"**
Ajouter le header :
```
Authorization: Token YOUR_TOKEN
```

---

Tout est prêt ! Vous pouvez maintenant développer le frontend Vue.js pour consommer cette API 🎉
