# 🗺️ Guide Complet des Routes Django - Pour Débutants

## 📚 **Comprendre les Routes Django**

### **🤔 Qu'est-ce qu'une route ?**

Une **route** est comme une **adresse** sur le web. Quand vous tapez une URL dans le navigateur, Django cherche quelle fonction Python doit répondre.

**Analogie :**
```
Route = Adresse postale
View = La personne qui habite à cette adresse
Response = La réponse que cette personne vous donne
```

---

## 🔄 **Le Cycle Complet : De la Requête à la Réponse**

```
┌──────────────┐
│  FRONTEND    │  1. Envoie requête GET /api/attendance/
│  (Vue.js)    │     ────────────────────────────>
└──────────────┘                                   
                                                   ┌──────────────┐
                                                   │   DJANGO     │
                                                   │              │
                                                   │ 2. urls.py   │
                                                   │ Trouve route │
                                                   │              │
                                                   │ 3. views.py  │
                                                   │ Exécute code │
                                                   │              │
                                                   │ 4. models.py │
                                                   │ Base données │
                                                   │              │
                                                   │ 5. Retourne  │
                                                   │    JSON      │
                                                   └──────────────┘
┌──────────────┐                                   
│  FRONTEND    │  6. Reçoit la réponse
│  (Vue.js)    │     <────────────────────────────
└──────────────┘                                   
```

---

## 📁 **Architecture des Fichiers**

```
backend/
├── config/
│   └── urls.py              # 🔴 Point d'entrée PRINCIPAL
│
└── apps/
    └── attendance/
        ├── urls.py          # 🔵 Routes de l'app attendance
        ├── views.py         # 🟢 Logique métier (fonctions)
        ├── serializers.py   # 🟡 Transformation JSON
        └── models.py        # 🟣 Modèles de données
```

---

## 1️⃣ **URLs Principales (`config/urls.py`)**

### **Rôle :** Point d'entrée de TOUTES les routes

```python
# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),                          # Interface admin
    path('api/attendance/', include('apps.attendance.urls')), # Délègue à l'app
]
```

### **Explication ligne par ligne :**

```python
path('admin/', admin.site.urls)
```
- `'admin/'` → Toutes les URLs commençant par `/admin/`
- `admin.site.urls` → Django gère automatiquement

```python
path('api/attendance/', include('apps.attendance.urls'))
```
- `'api/attendance/'` → Préfixe pour toutes les routes
- `include(...)` → "Va chercher dans `apps/attendance/urls.py`"

**Résultat :** Toutes les routes de `attendance/urls.py` auront le préfixe `/api/attendance/`

---

## 2️⃣ **URLs de l'Application (`apps/attendance/urls.py`)**

### **Rôle :** Définit les routes spécifiques de l'application

```python
# apps/attendance/urls.py
from django.urls import path
from . import views  # Importer les views de ce dossier

app_name = 'attendance'  # Namespace (optionnel mais recommandé)

urlpatterns = [
    # Liste et création de pointages
    path('', views.AttendanceListCreateView.as_view(), name='attendance-list-create'),
    
    # Détail d'un pointage
    path('<int:pk>/', views.AttendanceDetailView.as_view(), name='attendance-detail'),
    
    # Pointages du jour
    path('today/', views.MyAttendanceTodayView.as_view(), name='my-attendance-today'),
    
    # Pointage rapide
    path('check-in/', views.QuickCheckInView.as_view(), name='quick-check-in'),
    path('check-out/', views.QuickCheckOutView.as_view(), name='quick-check-out'),
]
```

### **Comprendre les patterns :**

#### **a) Route simple :**
```python
path('today/', views.MyAttendanceTodayView.as_view(), name='my-attendance-today')
```
- `'today/'` → URL sera `/api/attendance/today/`
- `views.MyAttendanceTodayView.as_view()` → Appelle cette View
- `name='my-attendance-today'` → Nom interne (pour reverse URL)

#### **b) Route avec paramètre :**
```python
path('<int:pk>/', views.AttendanceDetailView.as_view(), name='attendance-detail')
```
- `<int:pk>` → **Paramètre dynamique** (nombre entier)
- Exemples :
  - `/api/attendance/1/` → `pk = 1`
  - `/api/attendance/42/` → `pk = 42`
- Django passe `pk` à la View automatiquement

---

## 3️⃣ **Views (`apps/attendance/views.py`)**

### **Rôle :** Contient la LOGIQUE métier

### **Type 1 : View Simple (APIView)**

```python
from rest_framework.views import APIView
from rest_framework.response import Response

class QuickCheckInView(APIView):
    """
    POST /api/attendance/check-in/
    Créer un pointage d'entrée
    """
    
    def post(self, request):
        # 1. Récupérer les données
        user = request.user
        notes = request.data.get('notes', '')
        
        # 2. Créer le pointage
        attendance = Attendance.objects.create(
            user=user,
            attendance_type=AttendanceType.CHECK_IN,
            notes=notes
        )
        
        # 3. Retourner la réponse JSON
        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data, status=201)
```

**Méthodes HTTP disponibles :**
```python
class MyView(APIView):
    def get(self, request):      # GET → Récupérer
        pass
    
    def post(self, request):     # POST → Créer
        pass
    
    def put(self, request):      # PUT → Modifier (complet)
        pass
    
    def patch(self, request):    # PATCH → Modifier (partiel)
        pass
    
    def delete(self, request):   # DELETE → Supprimer
        pass
```

### **Type 2 : View Générique**

Django REST Framework fournit des **classes prêtes à l'emploi** :

```python
from rest_framework import generics

class AttendanceListCreateView(generics.ListCreateAPIView):
    """
    GET → Liste de tous les pointages
    POST → Créer un nouveau pointage
    """
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
```

**Moins de code, même résultat !**

**Vues génériques disponibles :**
- `ListAPIView` → GET liste
- `CreateAPIView` → POST création
- `RetrieveAPIView` → GET détail
- `UpdateAPIView` → PUT/PATCH modification
- `DestroyAPIView` → DELETE suppression
- `ListCreateAPIView` → GET liste + POST création
- `RetrieveUpdateDestroyAPIView` → GET/PUT/PATCH/DELETE

---

## 4️⃣ **Serializers (`apps/attendance/serializers.py`)**

### **Rôle :** Transformer les modèles Django en JSON (et vice-versa)

```python
from rest_framework import serializers
from .models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    # Champs supplémentaires (calculés)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Attendance
        fields = ['id', 'user', 'user_username', 'attendance_type', 'timestamp', 'date']
        read_only_fields = ['timestamp', 'date']
```

**Transformation automatique :**

```python
# Objet Python (modèle Django)
attendance = Attendance.objects.first()

# Conversion en JSON
serializer = AttendanceSerializer(attendance)
print(serializer.data)
```

**Résultat JSON :**
```json
{
  "id": 1,
  "user": 5,
  "user_username": "john",
  "attendance_type": "IN",
  "timestamp": "2025-10-23T08:30:00Z",
  "date": "2025-10-23"
}
```

---

## 📋 **Toutes les Routes Créées**

| URL | Méthode | Description |
|-----|---------|-------------|
| `/api/attendance/` | GET | Liste des pointages |
| `/api/attendance/` | POST | Créer un pointage |
| `/api/attendance/1/` | GET | Détail du pointage #1 |
| `/api/attendance/1/` | PUT/PATCH | Modifier le pointage #1 |
| `/api/attendance/1/` | DELETE | Supprimer le pointage #1 |
| `/api/attendance/today/` | GET | Mes pointages du jour |
| `/api/attendance/check-in/` | POST | Pointer l'entrée rapidement |
| `/api/attendance/check-out/` | POST | Pointer la sortie rapidement |
| `/api/attendance/stats/` | GET | Statistiques de pointage |
| `/api/attendance/sessions/` | GET | Sessions de travail |
| `/api/attendance/notifications/` | GET | Mes notifications |
| `/api/attendance/notifications/1/` | GET | Détail notification #1 |
| `/api/attendance/notifications/1/mark-read/` | POST | Marquer comme lu |
| `/api/attendance/notifications/mark-all-read/` | POST | Tout marquer comme lu |
| `/api/attendance/notifications/unread-count/` | GET | Nombre de non lus |
| `/api/attendance/settings/` | GET | Mes paramètres |
| `/api/attendance/settings/` | PUT/PATCH | Modifier mes paramètres |

---

## 🧪 **Tester les Routes**

### **Méthode 1 : Navigateur (GET uniquement)**
```
http://localhost:8000/api/attendance/
```

### **Méthode 2 : Curl**
```bash
# GET - Liste des pointages
curl http://localhost:8000/api/attendance/

# POST - Créer un pointage
curl -X POST http://localhost:8000/api/attendance/check-in/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{"notes": "Arrivée au bureau"}'
```

### **Méthode 3 : Interface Django REST (Navigateur)**
Django REST Framework fournit une **interface graphique** automatique :
```
http://localhost:8000/api/attendance/
```

---

## 🔐 **Authentification**

```python
from rest_framework.permissions import IsAuthenticated

class MyView(APIView):
    permission_classes = [IsAuthenticated]  # ✅ Requiert connexion
```

**Options d'authentification :**
- `AllowAny` → Tout le monde
- `IsAuthenticated` → Utilisateur connecté
- `IsAdminUser` → Utilisateur admin
- `IsAuthenticatedOrReadOnly` → Lecture publique, modification authentifiée

---

## 🎯 **Récapitulatif : Comment Créer une Route**

### **Étape 1 : Créer le Serializer**
```python
# serializers.py
class MySerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = ['id', 'name', 'date']
```

### **Étape 2 : Créer la View**
```python
# views.py
class MyView(generics.ListCreateAPIView):
    queryset = MyModel.objects.all()
    serializer_class = MySerializer
```

### **Étape 3 : Ajouter l'URL**
```python
# urls.py (de l'app)
urlpatterns = [
    path('my-route/', MyView.as_view(), name='my-route'),
]
```

### **Étape 4 : Inclure dans les URLs principales**
```python
# config/urls.py
urlpatterns = [
    path('api/myapp/', include('apps.myapp.urls')),
]
```

---

## 🚀 **Prochaines Étapes**

1. **Installer Django REST Framework** :
```bash
pip install djangorestframework
```

2. **Activer dans settings** :
```python
INSTALLED_APPS = [
    'rest_framework',
]
```

3. **Décommenter les routes** dans `config/urls.py`

4. **Créer les migrations** :
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Tester** :
```bash
python manage.py runserver
# Aller sur http://localhost:8000/api/attendance/
```

---

Vous avez maintenant tout compris sur les routes Django ! 🎉
