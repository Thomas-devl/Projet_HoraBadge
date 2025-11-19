"""
Views for users app
"""

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import Team
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    TeamSerializer,
    TeamDetailSerializer,
)

User = get_user_model()


# ============================================
# USERS VIEWS
# ============================================

class UserListCreateView(generics.ListCreateAPIView):
    """
    GET /users - Liste tous les utilisateurs
    POST /users - Créer un nouvel utilisateur
    """
    queryset = User.objects.all().order_by('-date_joined')
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Utiliser différents serializers selon la méthode"""
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer
    
    def get_queryset(self):
        """Filtrer les utilisateurs selon les query params"""
        queryset = super().get_queryset()
        
        # Recherche par nom, email ou username
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        
        # Filtrer par équipe
        team_id = self.request.query_params.get('team')
        if team_id:
            queryset = queryset.filter(team__id=team_id)
        
        # Filtrer par statut actif
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /users/{id} - Détail d'un utilisateur
    PUT /users/{id} - Modifier un utilisateur (complet)
    PATCH /users/{id} - Modifier un utilisateur (partiel)
    DELETE /users/{id} - Supprimer un utilisateur (avec query param ?permanent=true pour suppression définitive)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        """Seuls les admins peuvent supprimer"""
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def perform_destroy(self, instance):
        """
        Désactiver par défaut, supprimer définitivement si ?permanent=true
        """
        permanent = self.request.query_params.get('permanent', 'false').lower() == 'true'
        
        if permanent:
            # Suppression physique
            instance.delete()
        else:
            # Suppression logique (désactivation)
            instance.is_active = False
            instance.save()
    
    def destroy(self, request, *args, **kwargs):
        """Override pour retourner un message personnalisé"""
        instance = self.get_object()
        permanent = request.query_params.get('permanent', 'false').lower() == 'true'
        
        self.perform_destroy(instance)
        
        if permanent:
            return Response(
                {'message': 'Utilisateur supprimé définitivement'},
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            return Response(
                {'message': 'Utilisateur désactivé'},
                status=status.HTTP_200_OK
            )


class UserClocksView(APIView):
    """
    GET /users/{id}/clocks - Récupérer le résumé des pointages d'un utilisateur
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        """Récupérer les pointages d'un utilisateur"""
        from apps.attendance.models import Attendance
        from apps.attendance.serializers import AttendanceSerializer
        from datetime import datetime, timedelta
        
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {'error': 'Utilisateur non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Vérifier les permissions (admin ou soi-même)
        if not request.user.is_staff and request.user.id != user.id:
            return Response(
                {'error': 'Vous n\'avez pas la permission de voir ces données'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Paramètres de filtrage
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        # Par défaut : 30 derniers jours
        if not start_date:
            start_date = (datetime.now().date() - timedelta(days=30)).isoformat()
        if not end_date:
            end_date = datetime.now().date().isoformat()
        
        # Récupérer les pointages
        attendances = Attendance.objects.filter(
            user=user,
            date__gte=start_date,
            date__lte=end_date
        ).order_by('-timestamp')
        
        serializer = AttendanceSerializer(attendances, many=True)
        
        return Response({
            'user': UserSerializer(user).data,
            'period': {
                'start_date': start_date,
                'end_date': end_date,
            },
            'total_attendances': attendances.count(),
            'attendances': serializer.data,
        })


# ============================================
# TEAMS VIEWS
# ============================================

class TeamListCreateView(generics.ListCreateAPIView):
    """
    GET /teams - Liste toutes les équipes
    POST /teams - Créer une nouvelle équipe
    """
    queryset = Team.objects.all().order_by('-created_at')
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filtrer les équipes selon les query params"""
        queryset = super().get_queryset()
        
        # Recherche par nom
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        # Filtrer par manager
        manager_id = self.request.query_params.get('manager')
        if manager_id:
            queryset = queryset.filter(manager_id=manager_id)
        
        return queryset


class TeamDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /teams/{id} - Détail d'une équipe
    PUT /teams/{id} - Modifier une équipe (complet)
    PATCH /teams/{id} - Modifier une équipe (partiel)
    DELETE /teams/{id} - Supprimer une équipe
    """
    queryset = Team.objects.all()
    serializer_class = TeamDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        """Seuls les admins peuvent modifier/supprimer"""
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]


class TeamMembersView(APIView):
    """
    POST /teams/{id}/members - Ajouter des membres à une équipe
    DELETE /teams/{id}/members - Retirer des membres d'une équipe
    """
    permission_classes = [IsAdminUser]
    
    def post(self, request, pk):
        """Ajouter des membres"""
        try:
            team = Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            return Response(
                {'error': 'Équipe non trouvée'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        user_ids = request.data.get('user_ids', [])
        if not user_ids:
            return Response(
                {'error': 'user_ids requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        users = User.objects.filter(id__in=user_ids)
        team.members.add(*users)
        
        serializer = TeamDetailSerializer(team)
        return Response(serializer.data)
    
    def delete(self, request, pk):
        """Retirer des membres"""
        try:
            team = Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            return Response(
                {'error': 'Équipe non trouvée'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        user_ids = request.data.get('user_ids', [])
        if not user_ids:
            return Response(
                {'error': 'user_ids requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        users = User.objects.filter(id__in=user_ids)
        team.members.remove(*users)
        
        serializer = TeamDetailSerializer(team)
        return Response(serializer.data)


class MyTeamInfoView(APIView):
    """
    GET: Récupère les informations de l'équipe de l'utilisateur connecté
    Retourne: équipe, manager, et co-équipiers
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # Récupérer la (les) équipe(s) de l'utilisateur
        teams = user.teams.all()
        
        team_info = []
        for team in teams:
            team_data = {
                'id': team.id,
                'name': team.name,
                'description': team.description,
                'manager': None,
                'members_count': team.members.count(),
                'members': []
            }
            
            # Ajouter le manager s'il existe
            if team.manager:
                team_data['manager'] = {
                    'id': team.manager.id,
                    'username': team.manager.username,
                    'first_name': team.manager.first_name,
                    'last_name': team.manager.last_name,
                    'email': team.manager.email,
                    'function': team.manager.function
                }
            
            # Ajouter les co-équipiers
            for member in team.members.all():
                if member.id != user.id:  # Ne pas ajouter l'utilisateur lui-même
                    team_data['members'].append({
                        'id': member.id,
                        'username': member.username,
                        'first_name': member.first_name,
                        'last_name': member.last_name,
                        'function': member.function
                    })
            
            team_info.append(team_data)
        
        return Response({
            'team_count': len(teams),
            'teams': team_info
        })
