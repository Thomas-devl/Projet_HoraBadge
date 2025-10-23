"""
Views pour l'API Attendance
Gèrent la logique métier et les requêtes HTTP
"""
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta

from .models import Attendance, WorkSession, Notification, AttendanceSettings, AttendanceType
from .serializers import (
    AttendanceSerializer,
    AttendanceCreateSerializer,
    WorkSessionSerializer,
    NotificationSerializer,
    AttendanceSettingsSerializer
)


class AttendanceListCreateView(generics.ListCreateAPIView):
    """
    GET: Liste de tous les pointages
    POST: Créer un nouveau pointage
    """
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AttendanceCreateSerializer
        return AttendanceSerializer
    
    def get_queryset(self):
        user = self.request.user
        queryset = Attendance.objects.all()
        
        # Si pas admin, voir seulement ses propres pointages
        if not user.is_staff:
            queryset = queryset.filter(user=user)
        
        # Filtres optionnels
        date_filter = self.request.query_params.get('date', None)
        if date_filter:
            queryset = queryset.filter(date=date_filter)
        
        attendance_type = self.request.query_params.get('type', None)
        if attendance_type:
            queryset = queryset.filter(attendance_type=attendance_type)
        
        return queryset.order_by('-timestamp')


class AttendanceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Détail d'un pointage
    PUT/PATCH: Modifier un pointage
    DELETE: Supprimer un pointage
    """
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]


class MyAttendanceTodayView(APIView):
    """
    GET: Mes pointages du jour
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        today = timezone.now().date()
        attendances = Attendance.objects.filter(
            user=request.user,
            date=today
        ).order_by('timestamp')
        
        serializer = AttendanceSerializer(attendances, many=True)
        
        # Informations supplémentaires
        has_checked_in = attendances.filter(attendance_type=AttendanceType.CHECK_IN).exists()
        has_checked_out = attendances.filter(attendance_type=AttendanceType.CHECK_OUT).exists()
        
        return Response({
            'date': today,
            'attendances': serializer.data,
            'has_checked_in': has_checked_in,
            'has_checked_out': has_checked_out,
            'count': attendances.count()
        })


class QuickCheckInView(APIView):
    """
    POST: Pointage rapide d'entrée
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            attendance = Attendance.objects.create(
                user=request.user,
                attendance_type=AttendanceType.CHECK_IN,
                notes=request.data.get('notes', '')
            )
            serializer = AttendanceSerializer(attendance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class QuickCheckOutView(APIView):
    """
    POST: Pointage rapide de sortie
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            attendance = Attendance.objects.create(
                user=request.user,
                attendance_type=AttendanceType.CHECK_OUT,
                notes=request.data.get('notes', '')
            )
            serializer = AttendanceSerializer(attendance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class WorkSessionListView(generics.ListAPIView):
    """
    GET: Liste des sessions de travail
    """
    serializer_class = WorkSessionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = WorkSession.objects.all()
        
        if not user.is_staff:
            queryset = queryset.filter(user=user)
        
        # Filtrer par période
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        return queryset.order_by('-date')


class NotificationListView(generics.ListAPIView):
    """
    GET: Mes notifications
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Notification.objects.filter(user=user)
        
        # Filtrer par statut lu/non lu
        is_read = self.request.query_params.get('is_read', None)
        if is_read is not None:
            queryset = queryset.filter(is_read=is_read.lower() == 'true')
        
        return queryset.order_by('-created_at')


class NotificationDetailView(generics.RetrieveUpdateAPIView):
    """
    GET: Détail d'une notification
    PATCH: Marquer comme lu
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class NotificationMarkAsReadView(APIView):
    """
    POST: Marquer une notification comme lue
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, user=request.user)
            notification.mark_as_read()
            serializer = NotificationSerializer(notification)
            return Response(serializer.data)
        except Notification.DoesNotExist:
            return Response(
                {'error': 'Notification non trouvée'},
                status=status.HTTP_404_NOT_FOUND
            )


class NotificationMarkAllAsReadView(APIView):
    """
    POST: Marquer toutes les notifications comme lues
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).update(is_read=True, read_at=timezone.now())
        
        return Response({
            'message': f'{count} notification(s) marquée(s) comme lue(s)',
            'count': count
        })


class NotificationUnreadCountView(APIView):
    """
    GET: Nombre de notifications non lues
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()
        
        return Response({'count': count})


class AttendanceSettingsView(generics.RetrieveUpdateAPIView):
    """
    GET: Mes paramètres de pointage
    PUT/PATCH: Modifier mes paramètres
    """
    serializer_class = AttendanceSettingsSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        # Récupérer ou créer les paramètres de l'utilisateur
        obj, created = AttendanceSettings.objects.get_or_create(
            user=self.request.user
        )
        return obj


class AttendanceStatsView(APIView):
    """
    GET: Statistiques de pointage de l'utilisateur
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        today = timezone.now().date()
        
        # Pointages du jour
        today_attendances = Attendance.objects.filter(user=user, date=today)
        
        # Pointages de la semaine
        week_start = today - timedelta(days=today.weekday())
        week_attendances = Attendance.objects.filter(
            user=user,
            date__gte=week_start,
            date__lte=today
        )
        
        # Pointages du mois
        month_attendances = Attendance.objects.filter(
            user=user,
            date__year=today.year,
            date__month=today.month
        )
        
        # Sessions complètes du mois
        complete_sessions = WorkSession.objects.filter(
            user=user,
            date__year=today.year,
            date__month=today.month,
            is_complete=True
        )
        
        # Calculer le temps total travaillé
        total_hours = sum(
            session.duration.total_seconds() / 3600
            for session in complete_sessions
            if session.duration
        )
        
        return Response({
            'today': {
                'count': today_attendances.count(),
                'has_checked_in': today_attendances.filter(attendance_type=AttendanceType.CHECK_IN).exists(),
                'has_checked_out': today_attendances.filter(attendance_type=AttendanceType.CHECK_OUT).exists(),
            },
            'week': {
                'count': week_attendances.count(),
                'days_worked': week_attendances.values('date').distinct().count(),
            },
            'month': {
                'count': month_attendances.count(),
                'days_worked': month_attendances.values('date').distinct().count(),
                'complete_sessions': complete_sessions.count(),
                'total_hours': round(total_hours, 2),
            }
        })


class ClocksView(APIView):
    """
    POST /clocks - Pointer l'arrivée/départ de l'utilisateur authentifié
    Détermine automatiquement si c'est un check-in ou check-out
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Créer un pointage automatique (IN ou OUT selon le dernier)"""
        user = request.user
        today = timezone.now().date()
        
        # Récupérer le dernier pointage du jour
        last_attendance_today = Attendance.objects.filter(
            user=user,
            date=today
        ).order_by('-timestamp').first()
        
        # Déterminer le type de pointage
        if not last_attendance_today:
            # Pas de pointage aujourd'hui → CHECK_IN
            attendance_type = AttendanceType.CHECK_IN
        elif last_attendance_today.attendance_type == AttendanceType.CHECK_IN:
            # Dernier pointage = IN → CHECK_OUT
            attendance_type = AttendanceType.CHECK_OUT
        elif last_attendance_today.attendance_type == AttendanceType.CHECK_OUT:
            # Dernier pointage = OUT → CHECK_IN (retour de pause)
            attendance_type = AttendanceType.CHECK_IN
        else:
            # BREAK → CHECK_OUT (fin de pause)
            attendance_type = AttendanceType.CHECK_OUT
        
        # Récupérer les notes optionnelles
        notes = request.data.get('notes', '')
        
        # Créer le pointage
        attendance = Attendance.objects.create(
            user=user,
            attendance_type=attendance_type,
            notes=notes
        )
        
        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GlobalReportsView(APIView):
    """
    GET /reports - Récupérer un rapport global basé sur les KPIs choisis
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Générer un rapport global"""
        from django.contrib.auth import get_user_model
        from django.db.models import Count, Avg, Sum
        from datetime import datetime, timedelta
        
        User = get_user_model()
        
        # Paramètres de filtrage
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        team_id = request.query_params.get('team_id')
        user_id = request.query_params.get('user_id')
        
        # Par défaut : mois en cours
        if not start_date:
            start_date = timezone.now().date().replace(day=1).isoformat()
        if not end_date:
            end_date = timezone.now().date().isoformat()
        
        # Base queryset
        attendances = Attendance.objects.filter(
            date__gte=start_date,
            date__lte=end_date
        )
        
        # Filtrer par équipe
        if team_id:
            attendances = attendances.filter(user__team__id=team_id)
        
        # Filtrer par utilisateur
        if user_id:
            attendances = attendances.filter(user_id=user_id)
        
        # Permissions : non-admin = seulement soi-même
        if not request.user.is_staff:
            attendances = attendances.filter(user=request.user)
        
        # KPIs globaux
        total_attendances = attendances.count()
        total_users = attendances.values('user').distinct().count()
        total_check_ins = attendances.filter(attendance_type=AttendanceType.CHECK_IN).count()
        total_check_outs = attendances.filter(attendance_type=AttendanceType.CHECK_OUT).count()
        
        # Sessions de travail complètes
        work_sessions = WorkSession.objects.filter(
            user__in=attendances.values('user'),
            check_in__date__gte=start_date,
            check_in__date__lte=end_date
        )
        
        # Calcul des heures totales
        total_hours = 0
        for session in work_sessions:
            if session.duration:
                total_hours += session.duration.total_seconds() / 3600
        
        # Moyenne d'heures par utilisateur
        avg_hours_per_user = total_hours / total_users if total_users > 0 else 0
        
        # Top utilisateurs par nombre de pointages
        top_users = attendances.values('user__username', 'user__first_name', 'user__last_name')\
            .annotate(count=Count('id'))\
            .order_by('-count')[:10]
        
        # Statistiques par jour
        daily_stats = attendances.values('date')\
            .annotate(
                total=Count('id'),
                check_ins=Count('id', filter=Q(attendance_type=AttendanceType.CHECK_IN)),
                check_outs=Count('id', filter=Q(attendance_type=AttendanceType.CHECK_OUT))
            )\
            .order_by('date')
        
        # Notifications non lues (global pour admin)
        if request.user.is_staff:
            unread_notifications = Notification.objects.filter(is_read=False).count()
        else:
            unread_notifications = Notification.objects.filter(
                user=request.user,
                is_read=False
            ).count()
        
        return Response({
            'period': {
                'start_date': start_date,
                'end_date': end_date,
            },
            'global_kpis': {
                'total_attendances': total_attendances,
                'total_users': total_users,
                'total_check_ins': total_check_ins,
                'total_check_outs': total_check_outs,
                'complete_work_sessions': work_sessions.count(),
                'total_hours_worked': round(total_hours, 2),
                'avg_hours_per_user': round(avg_hours_per_user, 2),
                'unread_notifications': unread_notifications,
            },
            'top_users': list(top_users),
            'daily_statistics': list(daily_stats),
            'filters_applied': {
                'team_id': team_id,
                'user_id': user_id,
            }
        })
