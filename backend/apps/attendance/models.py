from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone


class AttendanceType(models.TextChoices):
    """Types de pointage"""
    CHECK_IN = 'IN', 'Entrée'
    CHECK_OUT = 'OUT', 'Sortie'
    BREAK_START = 'BREAK_START', 'Début pause'
    BREAK_END = 'BREAK_END', 'Fin pause'


class AttendanceStatus(models.TextChoices):
    """Statuts de pointage"""
    PENDING = 'PENDING', 'En attente'
    APPROVED = 'APPROVED', 'Validé'
    REJECTED = 'REJECTED', 'Rejeté'


class Attendance(models.Model):
    """Modèle pour gérer les pointages des utilisateurs"""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='attendances',
        verbose_name='Utilisateur'
    )
    
    attendance_type = models.CharField(
        max_length=20,
        choices=AttendanceType.choices,
        verbose_name='Type de pointage'
    )
    
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date et heure'
    )
    
    date = models.DateField(
        auto_now_add=True,
        verbose_name='Date',
        db_index=True
    )
    
    status = models.CharField(
        max_length=20,
        choices=AttendanceStatus.choices,
        default=AttendanceStatus.PENDING,
        verbose_name='Statut'
    )
    
    notes = models.TextField(
        blank=True,
        verbose_name='Notes/Commentaires'
    )
    
    validated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='validated_attendances',
        verbose_name='Validé par'
    )
    
    validated_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Date de validation'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Créé le'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Modifié le'
    )
    
    class Meta:
        db_table = 'attendances'
        verbose_name = 'Pointage'
        verbose_name_plural = 'Pointages'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['date', 'attendance_type']),
        ]
        
    def __str__(self):
        return f"{self.user.username} - {self.get_attendance_type_display()} - {self.timestamp.strftime('%d/%m/%Y %H:%M')}"
    
    def clean(self):
        """Validation personnalisée"""
        if self.pk is None:
            last_attendance = Attendance.objects.filter(
                user=self.user,
                date=self.date
            ).order_by('-timestamp').first()
            
            if last_attendance:
                if self.attendance_type == AttendanceType.CHECK_IN and last_attendance.attendance_type == AttendanceType.CHECK_IN:
                    raise ValidationError("Vous avez déjà pointé une entrée aujourd'hui.")
                
                if self.attendance_type == AttendanceType.CHECK_OUT and last_attendance.attendance_type != AttendanceType.CHECK_IN:
                    raise ValidationError("Vous devez d'abord pointer une entrée.")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class WorkSession(models.Model):
    """Modèle pour calculer les sessions de travail"""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='work_sessions',
        verbose_name='Utilisateur'
    )
    
    check_in = models.OneToOneField(
        Attendance,
        on_delete=models.CASCADE,
        related_name='session_check_in',
        verbose_name='Pointage entrée'
    )
    
    check_out = models.OneToOneField(
        Attendance,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='session_check_out',
        verbose_name='Pointage sortie'
    )
    
    date = models.DateField(
        verbose_name='Date',
        db_index=True
    )
    
    duration = models.DurationField(
        null=True,
        blank=True,
        verbose_name='Durée totale'
    )
    
    break_duration = models.DurationField(
        null=True,
        blank=True,
        verbose_name='Durée des pauses'
    )
    
    is_complete = models.BooleanField(
        default=False,
        verbose_name='Session complète'
    )
    
    class Meta:
        db_table = 'work_sessions'
        verbose_name = 'Session de travail'
        verbose_name_plural = 'Sessions de travail'
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user.username} - {self.date} ({self.duration or 'En cours'})"
    
    def calculate_duration(self):
        """Calculer la durée de la session"""
        if self.check_in and self.check_out:
            self.duration = self.check_out.timestamp - self.check_in.timestamp
            self.is_complete = True
        else:
            self.duration = None
            self.is_complete = False
        self.save()


class NotificationType(models.TextChoices):
    """Types de notifications"""
    MISSING_CHECK_IN = 'MISSING_CHECK_IN', 'Pointage d\'entrée manquant'
    MISSING_CHECK_OUT = 'MISSING_CHECK_OUT', 'Pointage de sortie manquant'
    LATE_CHECK_IN = 'LATE_CHECK_IN', 'Retard à l\'entrée'
    EARLY_CHECK_OUT = 'EARLY_CHECK_OUT', 'Sortie anticipée'
    VALIDATION_REQUIRED = 'VALIDATION_REQUIRED', 'Validation requise'
    VALIDATION_APPROVED = 'VALIDATION_APPROVED', 'Pointage validé'
    VALIDATION_REJECTED = 'VALIDATION_REJECTED', 'Pointage rejeté'


class Notification(models.Model):
    """Modèle pour les notifications de pointage"""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Utilisateur'
    )
    
    notification_type = models.CharField(
        max_length=30,
        choices=NotificationType.choices,
        verbose_name='Type de notification'
    )
    
    title = models.CharField(
        max_length=200,
        verbose_name='Titre'
    )
    
    message = models.TextField(
        verbose_name='Message'
    )
    
    attendance = models.ForeignKey(
        Attendance,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications',
        verbose_name='Pointage concerné'
    )
    
    is_read = models.BooleanField(
        default=False,
        verbose_name='Lu'
    )
    
    read_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Lu le'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Créé le'
    )
    
    class Meta:
        db_table = 'notifications'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    def mark_as_read(self):
        """Marquer la notification comme lue"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()


class AttendanceSettings(models.Model):
    """Paramètres de pointage par utilisateur ou équipe"""
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='attendance_settings',
        verbose_name='Utilisateur'
    )
    
    team = models.ForeignKey(
        'users.Team',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='attendance_settings',
        verbose_name='Équipe'
    )
    
    expected_check_in_time = models.TimeField(
        default='09:00',
        verbose_name='Heure d\'arrivée attendue'
    )
    
    expected_check_out_time = models.TimeField(
        default='17:00',
        verbose_name='Heure de départ attendue'
    )
    
    tolerance_minutes = models.IntegerField(
        default=15,
        verbose_name='Tolérance (minutes)'
    )
    
    notify_missing_check_in = models.BooleanField(
        default=True,
        verbose_name='Notifier entrée manquante'
    )
    
    notify_missing_check_out = models.BooleanField(
        default=True,
        verbose_name='Notifier sortie manquante'
    )
    
    notify_manager = models.BooleanField(
        default=True,
        verbose_name='Notifier le manager'
    )
    
    class Meta:
        db_table = 'attendance_settings'
        verbose_name = 'Paramètre de pointage'
        verbose_name_plural = 'Paramètres de pointage'
    
    def __str__(self):
        if self.user:
            return f"Paramètres de {self.user.username}"
        elif self.team:
            return f"Paramètres de l'équipe {self.team.name}"
        return "Paramètres de pointage"
