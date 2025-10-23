# 🔧 Système de Monitoring - HoraBadge

## ✅ **Monitoring Visuel Installé !**

Un système complet de monitoring a été mis en place pour surveiller l'état de santé du backend.

---

## 🎯 **Accès au Dashboard**

### **Dashboard Visuel Principal**
```
http://localhost:8000/monitoring/
```

**Fonctionnalités :**
- ✅ Affichage visuel avec barres de progression colorées
- ✅ Rafraîchissement automatique toutes les 10 secondes
- ✅ Statut global (Healthy / Degraded)
- ✅ Métriques détaillées par composant

---

## 📊 **Routes de Monitoring**

### **1. Health Check Complet**
```
GET /api/health/
```

**Retourne :**
- Statut global du système
- État de la base de données
- État des modèles Django
- État des routes API
- Ressources système (CPU, RAM, Disque)
- État du cache

**Exemple de réponse :**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-23T14:00:00",
  "components": {
    "database": {
      "status": "healthy",
      "type": "postgresql",
      "tables_count": 16,
      "users_count": 1,
      "message": "✅ Base de données opérationnelle"
    },
    "system": {
      "status": "healthy",
      "cpu_percent": 25.5,
      "memory_percent": 45.2,
      "disk_percent": 60.1,
      "message": "✅ Ressources système OK"
    },
    "models": {
      "status": "healthy",
      "models": {
        "users": 1,
        "teams": 0,
        "attendances": 0,
        "work_sessions": 0,
        "notifications": 0
      }
    },
    "routes": {
      "status": "healthy",
      "total_routes": 30,
      "message": "✅ Routes configurées correctement"
    },
    "cache": {
      "status": "healthy",
      "message": "✅ Cache opérationnel"
    }
  }
}
```

---

### **2. Health Check Rapide**
```
GET /api/health/quick/
```

**Pour monitoring externe fréquent (ex: tous les 5 secondes)**

**Retourne :**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-23T14:00:00"
}
```

**Codes de réponse :**
- `200 OK` → Système opérationnel
- `503 Service Unavailable` → Système en erreur

---

### **3. Statistiques Détaillées**
```
GET /api/health/stats/
```

**Statistiques complètes du système**

**Retourne :**
```json
{
  "timestamp": "2025-10-23T14:00:00",
  "database": {
    "total_users": 1,
    "active_users": 1,
    "staff_users": 1,
    "total_teams": 0
  },
  "attendance": {
    "total_attendances": 0,
    "today": 0,
    "this_week": 0,
    "this_month": 0
  },
  "work_sessions": {
    "total": 0,
    "this_week": 0
  },
  "notifications": {
    "total": 0,
    "unread": 0
  },
  "system": {
    "python_version": "3.12.3",
    "django_version": "5.2.7",
    "debug_mode": true
  }
}
```

---

## 🎨 **Django Debug Toolbar (Développement)**

Activé automatiquement en mode développement !

**Accès :**
- Ouvrez n'importe quelle page HTML (ex: `/api/users/`)
- Une barre latérale apparaît à droite de l'écran

**Fonctionnalités :**
- 📊 Requêtes SQL (temps d'exécution, nombre)
- ⏱️ Performance des vues
- 🔍 Variables de template
- 📦 Middleware stack
- 🌐 Headers HTTP
- ⚙️ Settings Django

---

## 📦 **Packages Installés**

1. **django-debug-toolbar** - Toolbar de debug visuel
2. **django-health-check** - Health checks Django
3. **psutil** - Métriques système (CPU, RAM, Disque)

---

## 🚨 **Alertes et Seuils**

### **CPU**
- ✅ < 60% → Healthy
- ⚠️ 60-80% → Warning
- ❌ > 80% → Degraded

### **RAM**
- ✅ < 60% → Healthy
- ⚠️ 60-80% → Warning
- ❌ > 80% → Degraded

### **Disque**
- ✅ < 60% → Healthy
- ⚠️ 60-80% → Warning
- ❌ > 80% → Degraded

---

## 🔄 **Auto-Refresh**

Le dashboard se rafraîchit automatiquement toutes les **10 secondes**.

Vous pouvez aussi cliquer sur le bouton **"🔄 Rafraîchir"** pour une mise à jour manuelle.

---

## 🧪 **Tester le Monitoring**

### **1. Dashboard Visuel**
```bash
# Ouvrir dans le navigateur
http://localhost:8000/monitoring/
```

### **2. API Health Check**
```bash
curl http://localhost:8000/api/health/ | jq
```

### **3. Health Check Rapide**
```bash
curl http://localhost:8000/api/health/quick/
```

### **4. Statistiques**
```bash
curl http://localhost:8000/api/health/stats/ | jq
```

---

## 🎯 **Cas d'Usage**

### **Monitoring Externe (Uptime Robot, Pingdom, etc.)**
```
Endpoint: http://votre-domaine.com/api/health/quick/
Intervalle: 5 minutes
Alert sur: Status Code != 200
```

### **Monitoring Interne (DevOps)**
```
Endpoint: http://votre-domaine.com/api/health/
Intervalle: 1 minute
Alert sur: status != "healthy"
```

### **Dashboard Équipe**
```
URL: http://votre-domaine.com/monitoring/
Affichage: Écran dédié dans le bureau
```

---

## 📈 **Métriques Surveillées**

| Composant | Métriques |
|-----------|-----------|
| **Base de données** | Type, Tables, Connexion, Utilisateurs |
| **Modèles** | Compteurs (Users, Teams, Attendances, etc.) |
| **Routes** | Nombre total, Routes critiques |
| **Système** | CPU %, RAM %, Disque % |
| **Cache** | Fonctionnalité, Écriture/Lecture |

---

## 🔐 **Sécurité**

### **Endpoints Publics (sans auth)**
- `/api/health/` - Pour monitoring externe
- `/api/health/quick/` - Pour ping rapide

### **Endpoints Protégés**
- `/api/health/stats/` - Authentification requise
- `/monitoring/` - Dashboard (recommandé : ajouter auth en prod)

**⚠️ En production, sécurisez `/monitoring/` avec authentification !**

---

## 🎨 **Personnalisation**

Le dashboard est entièrement personnalisable dans :
```
/backend/templates/monitoring_dashboard.html
```

Vous pouvez :
- Changer les couleurs
- Ajouter des graphiques
- Modifier les seuils d'alerte
- Ajouter d'autres métriques

---

## 📝 **Exemple d'Intégration**

### **Script de monitoring Python**
```python
import requests
import time

def check_health():
    try:
        response = requests.get('http://localhost:8000/api/health/')
        data = response.json()
        
        if data['status'] != 'healthy':
            # Envoyer alerte (email, Slack, etc.)
            send_alert(f"⚠️ Backend dégradé : {data}")
        
        return data
    except Exception as e:
        send_alert(f"❌ Backend inaccessible : {e}")

# Vérifier toutes les 60 secondes
while True:
    check_health()
    time.sleep(60)
```

---

## ✨ **Résumé**

| Fonctionnalité | URL | Status |
|----------------|-----|--------|
| Dashboard Visuel | `/monitoring/` | ✅ |
| Health Check API | `/api/health/` | ✅ |
| Quick Check | `/api/health/quick/` | ✅ |
| Stats Détaillées | `/api/health/stats/` | ✅ |
| Debug Toolbar | `/__debug__/` | ✅ (dev only) |

---

## 🚀 **Accès Rapide**

**Dashboard Principal :**
```
http://localhost:8000/monitoring/
```

**API Health :**
```
http://localhost:8000/api/health/
```

**Le monitoring est maintenant opérationnel ! 🎉**
