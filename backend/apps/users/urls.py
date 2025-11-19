"""
URL configuration for users app
"""

from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Users endpoints
    path('users/', views.UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('users/<int:pk>/clocks/', views.UserClocksView.as_view(), name='user-clocks'),
    path('users/me/team-info/', views.MyTeamInfoView.as_view(), name='my-team-info'),
    
    # Teams endpoints
    path('teams/', views.TeamListCreateView.as_view(), name='team-list-create'),
    path('teams/<int:pk>/', views.TeamDetailView.as_view(), name='team-detail'),
    path('teams/<int:pk>/members/', views.TeamMembersView.as_view(), name='team-members'),
]
