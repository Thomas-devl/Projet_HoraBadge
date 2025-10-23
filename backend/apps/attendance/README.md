# Système de Notifications pour Pointages

## 📋 **Fonctionnalités**

### ✅ **1. Notifications automatiques**
Le système crée automatiquement des notifications pour :
- **Pointage d'entrée manquant** : Si l'utilisateur n'a pas pointé son entrée
- **Pointage de sortie manquant** : Si l'utilisateur n'a pas pointé sa sortie après avoir pointé l'entrée
- **Rappel** : Notification automatique après le pointage d'entrée pour ne pas oublier la sortie

### ✅ **2. Types de notifications**
- `MISSING_CHECK_IN` : Pointage d'entrée manquant
- `MISSING_CHECK_OUT` : Pointage de sortie manquant
- `LATE_CHECK_IN` : Retard à l'entrée
- `EARLY_CHECK_OUT` : Sortie anticipée
- `VALIDATION_REQUIRED` : Validation requise
- `VALIDATION_APPROVED` : Pointage validé
- `VALIDATION_REJECTED` : Pointage rejeté

### ✅ **3. Paramètres personnalisables**
Chaque utilisateur ou équipe peut configurer :
- Heure d'arrivée attendue
- Heure de départ attendue
- Tolérance en minutes
- Activer/désactiver les notifications
- Notifier le manager

---

## 🚀 **Utilisation**

### **1. Vérifier les pointages manquants manuellement**
```bash
python manage.py check_missing_attendance
```

### **2. Vérifier pour une date spécifique**
```bash
python manage.py check_missing_attendance --date 2025-10-22
```

### **3. Avec notification des managers**
```bash
python manage.py check_missing_attendance --notify-managers
```

---

## ⏰ **Automatisation avec Cron**

### **Linux/Mac - Crontab**
Ajouter dans `crontab -e` :

```bash
# Vérifier les pointages manquants tous les jours à 20h
0 20 * * * cd /path/to/backend && python manage.py check_missing_attendance --notify-managers

# Vérifier tous les lundis à 9h pour le week-end
0 9 * * 1 cd /path/to/backend && python manage.py check_missing_attendance --notify-managers
```

### **Django-celery-beat (Recommandé en production)**

1. Installer celery-beat :
```bash
pip install celery django-celery-beat
```

2. Configurer la tâche périodique dans `settings.py` :
```python
CELERY_BEAT_SCHEDULE = {
    'check-missing-attendance-daily': {
        'task': 'apps.attendance.tasks.check_missing_attendance',
        'schedule': crontab(hour=20, minute=0),  # Tous les jours à 20h
    },
}
```

---

## 💻 **Utilisation dans le code**

### **Créer une notification manuellement**
```python
from apps.attendance.models import Notification, NotificationType

Notification.objects.create(
    user=user,
    notification_type=NotificationType.MISSING_CHECK_IN,
    title="Pointage manquant",
    message="Vous n'avez pas pointé aujourd'hui."
)
```

### **Marquer comme lue**
```python
notification = Notification.objects.get(id=1)
notification.mark_as_read()
```

### **Récupérer les notifications non lues**
```python
unread = user.notifications.filter(is_read=False)
count = user.notifications.filter(is_read=False).count()
```

### **Configurer les paramètres d'un utilisateur**
```python
from apps.attendance.models import AttendanceSettings
from datetime import time

AttendanceSettings.objects.create(
    user=user,
    expected_check_in_time=time(9, 0),  # 09:00
    expected_check_out_time=time(17, 0),  # 17:00
    tolerance_minutes=15,
    notify_missing_check_in=True,
    notify_missing_check_out=True,
    notify_manager=True
)
```

---

## 📊 **Workflow des notifications**

```
1. Utilisateur pointe l'entrée (08:00)
   ↓
2. Signal Django crée une notification de rappel
   "N'oubliez pas de pointer votre sortie"
   ↓
3. Fin de journée (20:00)
   ↓
4. Commande check_missing_attendance s'exécute
   ↓
5. Vérification : sortie pointée ?
   ↓
   NON → Créer notification "Sortie manquante"
   ↓
6. Si paramètre activé → Notifier le manager
```

---

## 🔔 **Interface Admin**

### **Gérer les notifications**
- Voir toutes les notifications
- Filtrer par type, utilisateur, date
- Marquer comme lu/non lu
- Actions groupées

### **Paramètres de pointage**
- Configurer par utilisateur ou équipe
- Horaires attendus
- Tolérance
- Préférences de notification

---

## 🎯 **Bonnes pratiques**

1. **Activer les notifications progressivement** : Commencer par quelques utilisateurs
2. **Ajuster la tolérance** : 15 minutes est un bon début
3. **Exécuter la vérification en soirée** : Après la journée de travail
4. **Ne pas spammer** : Une notification par événement
5. **Permettre la désactivation** : Certains utilisateurs peuvent ne pas vouloir de notifications

---

## 📝 **Exemples de notifications**

### **Entrée manquante**
```
Titre: Pointage d'entrée manquant
Message: Vous n'avez pas pointé votre entrée le 23/10/2025. 
         Veuillez régulariser votre situation.
```

### **Sortie manquante**
```
Titre: Pointage de sortie manquant
Message: Vous n'avez pas pointé votre sortie le 23/10/2025. 
         Dernière entrée: 08:30.
```

### **Notification au manager**
```
Titre: Alerte pointage - John Doe
Message: John Doe n'a pas pointé son entrée le 23/10/2025.
```

---

## 🔧 **Développements futurs possibles**

- ✉️ Notifications par email
- 📱 Notifications push (mobile)
- 📊 Dashboard des pointages
- 📈 Statistiques d'assiduité
- 🤖 IA pour détecter les patterns anormaux
- 📅 Intégration calendrier (congés, jours fériés)
