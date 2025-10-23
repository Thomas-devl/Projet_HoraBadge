"""
URLs pour l'API Attendance
Définit toutes les routes de l'application
"""
from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    # ========== POINTAGES ==========
    # Liste et création de pointages
    path('', views.AttendanceListCreateView.as_view(), name='attendance-list-create'),
    
    # Détail, modification, suppression d'un pointage
    path('<int:pk>/', views.AttendanceDetailView.as_view(), name='attendance-detail'),
    
    # Mes pointages du jour
    path('today/', views.MyAttendanceTodayView.as_view(), name='my-attendance-today'),
    
    # Pointage rapide
    path('check-in/', views.QuickCheckInView.as_view(), name='quick-check-in'),
    path('check-out/', views.QuickCheckOutView.as_view(), name='quick-check-out'),
    
    # Statistiques
    path('stats/', views.AttendanceStatsView.as_view(), name='attendance-stats'),
    
    
    # ========== SESSIONS DE TRAVAIL ==========
    path('sessions/', views.WorkSessionListView.as_view(), name='work-session-list'),
    
    
    # ========== NOTIFICATIONS ==========
    # Liste des notifications
    path('notifications/', views.NotificationListView.as_view(), name='notification-list'),
    
    # Détail d'une notification
    path('notifications/<int:pk>/', views.NotificationDetailView.as_view(), name='notification-detail'),
    
    # Marquer comme lu
    path('notifications/<int:pk>/mark-read/', views.NotificationMarkAsReadView.as_view(), name='notification-mark-read'),
    
    # Marquer tout comme lu
    path('notifications/mark-all-read/', views.NotificationMarkAllAsReadView.as_view(), name='notification-mark-all-read'),
    
    # Nombre de notifications non lues
    path('notifications/unread-count/', views.NotificationUnreadCountView.as_view(), name='notification-unread-count'),
    
    
    # ========== PARAMÈTRES ==========
    path('settings/', views.AttendanceSettingsView.as_view(), name='attendance-settings'),
    
    
    # ========== ROUTES SUPPLÉMENTAIRES ==========
    # Pointage automatique (détermine IN/OUT automatiquement)
    path('clocks/', views.ClocksView.as_view(), name='clocks'),
    
    # Rapport global avec KPIs
    path('reports/', views.GlobalReportsView.as_view(), name='global-reports'),
]
