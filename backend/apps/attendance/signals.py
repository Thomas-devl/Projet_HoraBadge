"""
Signals pour gérer les notifications de pointage
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from .models import Attendance, Notification, NotificationType, AttendanceType


@receiver(post_save, sender=Attendance)
def check_attendance_after_save(sender, instance, created, **kwargs):
    """
    Signal déclenché après la sauvegarde d'un pointage.
    Vérifie s'il manque un pointage de sortie.
    """
    if created and instance.attendance_type == AttendanceType.CHECK_IN:
        # Créer une notification pour rappeler de pointer la sortie
        create_reminder_notification(instance)


def create_reminder_notification(attendance):
    """
    Créer une notification de rappel pour pointer la sortie
    """
    # Vérifier si une notification similaire n'existe pas déjà
    existing = Notification.objects.filter(
        user=attendance.user,
        notification_type=NotificationType.MISSING_CHECK_OUT,
        attendance=attendance,
        is_read=False
    ).exists()
    
    if not existing:
        Notification.objects.create(
            user=attendance.user,
            notification_type=NotificationType.MISSING_CHECK_OUT,
            title="N'oubliez pas de pointer votre sortie",
            message=f"Vous avez pointé votre entrée à {attendance.timestamp.strftime('%H:%M')}. N'oubliez pas de pointer votre sortie en fin de journée.",
            attendance=attendance
        )


def create_missing_check_in_notification(user, date):
    """
    Créer une notification pour un pointage d'entrée manquant
    """
    Notification.objects.create(
        user=user,
        notification_type=NotificationType.MISSING_CHECK_IN,
        title="Pointage d'entrée manquant",
        message=f"Vous n'avez pas pointé votre entrée le {date.strftime('%d/%m/%Y')}. Veuillez régulariser votre situation.",
    )


def create_missing_check_out_notification(user, attendance):
    """
    Créer une notification pour un pointage de sortie manquant
    """
    Notification.objects.create(
        user=user,
        notification_type=NotificationType.MISSING_CHECK_OUT,
        title="Pointage de sortie manquant",
        message=f"Vous n'avez pas pointé votre sortie le {attendance.date.strftime('%d/%m/%Y')}. Dernière entrée: {attendance.timestamp.strftime('%H:%M')}.",
        attendance=attendance
    )


def notify_manager(user, notification_type, message):
    """
    Notifier le manager de l'utilisateur
    """
    # Récupérer les équipes de l'utilisateur
    teams = user.teams.all()
    
    for team in teams:
        if team.manager and team.manager != user:
            Notification.objects.create(
                user=team.manager,
                notification_type=notification_type,
                title=f"Alerte pointage - {user.get_full_name() or user.username}",
                message=message
            )
