"""
Tests pour le système de notifications de pointage
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from apps.attendance.models import (
    Attendance,
    AttendanceType,
    Notification,
    NotificationType,
    AttendanceSettings
)

User = get_user_model()


class AttendanceNotificationTestCase(TestCase):
    """Tests pour les notifications de pointage"""
    
    def setUp(self):
        """Préparer les données de test"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Créer les paramètres par défaut
        AttendanceSettings.objects.create(
            user=self.user,
            notify_missing_check_in=True,
            notify_missing_check_out=True
        )
    
    def test_check_in_creates_reminder(self):
        """Tester qu'un pointage d'entrée crée une notification de rappel"""
        # Créer un pointage d'entrée
        attendance = Attendance.objects.create(
            user=self.user,
            attendance_type=AttendanceType.CHECK_IN
        )
        
        # Vérifier qu'une notification a été créée
        notifications = Notification.objects.filter(
            user=self.user,
            notification_type=NotificationType.MISSING_CHECK_OUT
        )
        
        self.assertEqual(notifications.count(), 1)
        self.assertIn("sortie", notifications.first().message.lower())
    
    def test_notification_mark_as_read(self):
        """Tester le marquage comme lu"""
        notification = Notification.objects.create(
            user=self.user,
            notification_type=NotificationType.MISSING_CHECK_IN,
            title="Test",
            message="Test message"
        )
        
        self.assertFalse(notification.is_read)
        self.assertIsNone(notification.read_at)
        
        notification.mark_as_read()
        
        self.assertTrue(notification.is_read)
        self.assertIsNotNone(notification.read_at)
    
    def test_duplicate_check_in_validation(self):
        """Tester qu'on ne peut pas pointer deux entrées le même jour"""
        # Premier pointage d'entrée
        Attendance.objects.create(
            user=self.user,
            attendance_type=AttendanceType.CHECK_IN
        )
        
        # Tentative de second pointage d'entrée
        with self.assertRaises(Exception):
            Attendance.objects.create(
                user=self.user,
                attendance_type=AttendanceType.CHECK_IN
            )
