"""
Serializers pour l'API Attendance
Transforment les modèles Django en JSON et vice-versa
"""
from rest_framework import serializers
from .models import Attendance, WorkSession, Notification, AttendanceSettings


class AttendanceSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Attendance"""
    
    # Champs en lecture seule (calculés automatiquement)
    user_username = serializers.CharField(source='user.username', read_only=True)
    attendance_type_display = serializers.CharField(source='get_attendance_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Attendance
        fields = [
            'id',
            'user',
            'user_username',
            'attendance_type',
            'attendance_type_display',
            'timestamp',
            'date',
            'status',
            'status_display',
            'notes',
            'validated_by',
            'validated_at',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['timestamp', 'date', 'created_at', 'updated_at']


class AttendanceCreateSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour créer un pointage"""
    
    class Meta:
        model = Attendance
        fields = ['attendance_type', 'notes']
    
    def create(self, validated_data):
        # Ajouter automatiquement l'utilisateur connecté
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class WorkSessionSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle WorkSession"""
    
    user_username = serializers.CharField(source='user.username', read_only=True)
    check_in_time = serializers.CharField(source='check_in.timestamp', read_only=True)
    check_out_time = serializers.CharField(source='check_out.timestamp', read_only=True)
    
    class Meta:
        model = WorkSession
        fields = [
            'id',
            'user',
            'user_username',
            'check_in',
            'check_in_time',
            'check_out',
            'check_out_time',
            'date',
            'duration',
            'break_duration',
            'is_complete'
        ]
        read_only_fields = ['duration', 'is_complete']


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Notification"""
    
    notification_type_display = serializers.CharField(source='get_notification_type_display', read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id',
            'user',
            'notification_type',
            'notification_type_display',
            'title',
            'message',
            'attendance',
            'is_read',
            'read_at',
            'created_at'
        ]
        read_only_fields = ['created_at', 'read_at']


class AttendanceSettingsSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle AttendanceSettings"""
    
    class Meta:
        model = AttendanceSettings
        fields = [
            'id',
            'user',
            'team',
            'expected_check_in_time',
            'expected_check_out_time',
            'tolerance_minutes',
            'notify_missing_check_in',
            'notify_missing_check_out',
            'notify_manager'
        ]
