# 🗄️ Base de Données - PostgreSQL

## ✅ **BASE DE DONNÉES POSTGRESQL ACTIVE !**

Nom : **`horabadge_dev`**  
Moteur : **PostgreSQL**  
Utilisateur : **`horabadge_user`**

---

## 🔐 **Informations de Connexion**

### **Base de Données PostgreSQL**
```
Nom     : horabadge_dev
Host    : localhost
Port    : 5432
User    : horabadge_user
Password: horabadge2024
```

### **Superutilisateur Django**
```
Username: admin
Password: admin123
Email   : admin@horabadge.com
```

---

## 📊 **Tables Créées (16 tables)**

### **Tables Principales (Vos Modèles)**

| Table | Description | Modèle |
|-------|-------------|--------|
| ✅ `users` | Utilisateurs | `apps.users.models.User` |
| ✅ `teams` | Équipes | `apps.users.models.Team` |
| ✅ `attendances` | Pointages | `apps.attendance.models.Attendance` |
| ✅ `work_sessions` | Sessions de travail | `apps.attendance.models.WorkSession` |
| ✅ `notifications` | Notifications | `apps.attendance.models.Notification` |
| ✅ `attendance_settings` | Paramètres utilisateur | `apps.attendance.models.AttendanceSettings` |

### **Tables Intermédiaires (Relations Many-to-Many)**

| Table | Relation |
|-------|----------|
| ✅ `teams_members` | Team ↔ Users (membres) |
| ✅ `users_groups` | User ↔ Groups |
| ✅ `users_user_permissions` | User ↔ Permissions |

### **Tables Django (Système)**

| Table | Usage |
|-------|-------|
| ✅ `auth_group` | Groupes Django |
| ✅ `auth_group_permissions` | Permissions des groupes |
| ✅ `auth_permission` | Permissions Django |
| ✅ `django_admin_log` | Historique admin |
| ✅ `django_content_type` | Types de contenu |
| ✅ `django_migrations` | Historique migrations |
| ✅ `django_session` | Sessions utilisateur |

---

## 👤 **Utilisateurs Existants**

```
👥 Utilisateurs : 1
  - admin (admin@horabadge.com)
```

**Pour réinitialiser le mot de passe :**

```bash
cd /home/keirs/epitech/Projet_HoraBadge/backend
source venv/bin/activate
python manage.py changepassword admin
```

---

## 🔍 **Explorer la Base de Données**

### **Méthode 1 : Interface Admin Django** ⭐ **Recommandé**

1. **Lancer le serveur** (s'il n'est pas déjà lancé) :
   ```bash
   python manage.py runserver
   ```

2. **Ouvrir dans le navigateur** :
   ```
   http://localhost:8000/admin/
   ```

3. **Se connecter** :
   - Username : `admin`
   - Password : (votre mot de passe)

4. **Vous pouvez** :
   - ✅ Créer des utilisateurs
   - ✅ Créer des équipes
   - ✅ Créer des pointages
   - ✅ Voir les notifications
   - ✅ Modifier les paramètres

---

### **Méthode 2 : Django Shell**

```bash
python manage.py shell
```

**Exemples de requêtes :**

```python
# Importer les modèles
from django.contrib.auth import get_user_model
from apps.attendance.models import Attendance, Notification

User = get_user_model()

# Voir tous les utilisateurs
User.objects.all()

# Compter les pointages
Attendance.objects.count()

# Voir les notifications
Notification.objects.all()

# Créer un pointage
from apps.attendance.models import AttendanceType
user = User.objects.get(username='admin')
attendance = Attendance.objects.create(
    user=user,
    attendance_type=AttendanceType.CHECK_IN,
    notes="Test depuis le shell"
)
print(f"Pointage créé : {attendance}")
```

---

### **Méthode 3 : SQLite Browser** (Outil externe)

**Installer :**
```bash
sudo apt install sqlitebrowser  # Ubuntu/Debian
# ou
brew install --cask db-browser-for-sqlite  # macOS
```

**Ouvrir :**
```bash
sqlitebrowser db.sqlite3
```

---

### **Méthode 4 : Ligne de Commande SQLite**

```bash
sqlite3 db.sqlite3
```

**Commandes utiles :**
```sql
-- Lister les tables
.tables

-- Voir la structure d'une table
.schema users

-- Compter les utilisateurs
SELECT COUNT(*) FROM users;

-- Voir tous les pointages
SELECT * FROM attendances;

-- Quitter
.quit
```

---

## 📈 **Vérifier l'État de la Base**

### **Voir les migrations appliquées :**

```bash
python manage.py showmigrations
```

**Résultat :**
```
admin
 [X] 0001_initial
 [X] 0002_logentry_remove_auto_add
 [X] 0003_logentry_add_action_flag_choices
attendance
 [X] 0001_initial
 [X] 0002_initial
auth
 [X] 0001_initial
 ...
users
 [X] 0001_initial
```

---

### **Statistiques rapides :**

```bash
python manage.py shell -c "
from django.contrib.auth import get_user_model
from apps.attendance.models import Attendance, Notification, WorkSession

User = get_user_model()

print(f'👥 Utilisateurs : {User.objects.count()}')
print(f'📊 Pointages : {Attendance.objects.count()}')
print(f'🔔 Notifications : {Notification.objects.count()}')
print(f'💼 Sessions : {WorkSession.objects.count()}')
"
```

---

## 🔄 **Réinitialiser la Base (Si Nécessaire)**

### **⚠️ ATTENTION : Supprime toutes les données !**

```bash
# 1. Supprimer la base
rm db.sqlite3

# 2. Supprimer les fichiers de migration (optionnel)
rm apps/users/migrations/0*.py
rm apps/attendance/migrations/0*.py

# 3. Recréer les migrations
python manage.py makemigrations

# 4. Appliquer les migrations
python manage.py migrate

# 5. Créer un nouveau superutilisateur
python manage.py createsuperuser
```

---

## 🚀 **Peupler la Base avec des Données de Test**

Créez un fichier `scripts/populate_db.py` :

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.users.models import Team
from apps.attendance.models import Attendance, AttendanceType
from datetime import datetime, timedelta

User = get_user_model()

# Créer une équipe
team = Team.objects.create(
    name="Équipe Dev",
    description="Équipe de développement"
)

# Créer des utilisateurs
users = []
for i in range(1, 6):
    user = User.objects.create_user(
        username=f'user{i}',
        email=f'user{i}@horabadge.com',
        password='password123',
        function=f'Développeur {i}'
    )
    team.members.add(user)
    users.append(user)

# Définir un manager
team.manager = users[0]
team.save()

# Créer des pointages pour les 7 derniers jours
for user in users:
    for day in range(7):
        date = datetime.now().date() - timedelta(days=day)
        
        # Check-in
        Attendance.objects.create(
            user=user,
            attendance_type=AttendanceType.CHECK_IN,
            date=date,
            notes=f"Arrivée jour {day}"
        )
        
        # Check-out
        Attendance.objects.create(
            user=user,
            attendance_type=AttendanceType.CHECK_OUT,
            date=date,
            notes=f"Départ jour {day}"
        )

print("✅ Base de données peuplée avec succès !")
print(f"👥 {User.objects.count()} utilisateurs")
print(f"🏢 {Team.objects.count()} équipes")
print(f"📊 {Attendance.objects.count()} pointages")
```

**Exécuter :**
```bash
python scripts/populate_db.py
```

---

## 🎯 **Résumé**

| Élément | État | Commande |
|---------|------|----------|
| Base de données | ✅ **Existe** | `db.sqlite3` |
| Tables | ✅ **16 créées** | `python manage.py showmigrations` |
| Utilisateur admin | ✅ **Existe** | Username: `admin` |
| Migrations | ✅ **Appliquées** | `python manage.py migrate` |
| Serveur | ✅ **Fonctionne** | http://localhost:8000 |

---

## 🆘 **Commandes Utiles**

```bash
# Voir l'état des migrations
python manage.py showmigrations

# Créer des migrations après modif modèles
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Ouvrir le shell Django
python manage.py shell

# Créer un superutilisateur
python manage.py createsuperuser

# Changer mot de passe
python manage.py changepassword admin

# Lancer le serveur
python manage.py runserver

# Voir les statistiques
python manage.py shell -c "from django.contrib.auth import get_user_model; print(get_user_model().objects.count())"
```

---

**La base de données est prête et fonctionnelle ! 🎉**
