"""
Commande Django pour vérifier les pointages manquants.
À exécuter quotidiennement via un cron job ou un scheduler.

Usage: python manage.py check_missing_attendance
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta
from apps.attendance.models import (
    Attendance, 
    Notification, 
    NotificationType,
    AttendanceType,
    AttendanceSettings
)
from apps.attendance.signals import (
    create_missing_check_in_notification,
    create_missing_check_out_notification,
    notify_manager
)

User = get_user_model()


class Command(BaseCommand):
    help = 'Vérifie les pointages manquants et envoie des notifications'

    def add_arguments(self, parser):
        parser.add_argument(
            '--date',
            type=str,
            help='Date à vérifier (format: YYYY-MM-DD). Par défaut: hier',
        )
        parser.add_argument(
            '--notify-managers',
            action='store_true',
            help='Notifier également les managers',
        )

    def handle(self, *args, **options):
        # Déterminer la date à vérifier (par défaut: hier)
        if options['date']:
            from datetime import datetime
            check_date = datetime.strptime(options['date'], '%Y-%m-%d').date()
        else:
            check_date = timezone.now().date() - timedelta(days=1)
        
        self.stdout.write(f"🔍 Vérification des pointages manquants pour le {check_date.strftime('%d/%m/%Y')}")
        
        # Récupérer tous les utilisateurs actifs
        active_users = User.objects.filter(is_active=True)
        
        missing_check_in_count = 0
        missing_check_out_count = 0
        
        for user in active_users:
            # Vérifier les pointages de l'utilisateur pour cette date
            attendances = Attendance.objects.filter(
                user=user,
                date=check_date
            ).order_by('timestamp')
            
            # Récupérer les paramètres de l'utilisateur
            try:
                settings = user.attendance_settings
            except AttributeError:
                settings = None
            
            # 1. Vérifier si l'entrée manque
            check_in = attendances.filter(attendance_type=AttendanceType.CHECK_IN).first()
            
            if not check_in:
                # Vérifier si ce n'est pas un week-end ou jour férié
                if check_date.weekday() < 5:  # Lundi=0, Vendredi=4
                    if not settings or settings.notify_missing_check_in:
                        create_missing_check_in_notification(user, check_date)
                        missing_check_in_count += 1
                        
                        # Notifier le manager si activé
                        if options['notify_managers'] and settings and settings.notify_manager:
                            notify_manager(
                                user,
                                NotificationType.MISSING_CHECK_IN,
                                f"{user.get_full_name() or user.username} n'a pas pointé son entrée le {check_date.strftime('%d/%m/%Y')}."
                            )
                        
                        self.stdout.write(
                            self.style.WARNING(
                                f"  ⚠️  Entrée manquante: {user.username}"
                            )
                        )
            
            # 2. Vérifier si la sortie manque
            else:
                check_out = attendances.filter(attendance_type=AttendanceType.CHECK_OUT).first()
                
                if not check_out:
                    if not settings or settings.notify_missing_check_out:
                        create_missing_check_out_notification(user, check_in)
                        missing_check_out_count += 1
                        
                        # Notifier le manager si activé
                        if options['notify_managers'] and settings and settings.notify_manager:
                            notify_manager(
                                user,
                                NotificationType.MISSING_CHECK_OUT,
                                f"{user.get_full_name() or user.username} n'a pas pointé sa sortie le {check_date.strftime('%d/%m/%Y')}. Entrée: {check_in.timestamp.strftime('%H:%M')}."
                            )
                        
                        self.stdout.write(
                            self.style.WARNING(
                                f"  ⚠️  Sortie manquante: {user.username} (entrée à {check_in.timestamp.strftime('%H:%M')})"
                            )
                        )
        
        # Résumé
        self.stdout.write(
            self.style.SUCCESS(
                f"\n✅ Vérification terminée:"
            )
        )
        self.stdout.write(f"   - {missing_check_in_count} entrée(s) manquante(s)")
        self.stdout.write(f"   - {missing_check_out_count} sortie(s) manquante(s)")
        self.stdout.write(f"   - Total: {missing_check_in_count + missing_check_out_count} notification(s) créée(s)")
