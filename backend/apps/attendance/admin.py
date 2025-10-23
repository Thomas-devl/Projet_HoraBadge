from django.contrib import admin
from django.utils.html import format_html
from .models import Attendance, WorkSession, Notification, AttendanceSettings


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'attendance_type_badge', 'timestamp', 'status_badge', 'validated_by']
    list_filter = ['attendance_type', 'status', 'date', 'user']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['timestamp', 'date', 'created_at', 'updated_at']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('user', 'attendance_type', 'timestamp', 'date')
        }),
        ('Validation', {
            'fields': ('status', 'validated_by', 'validated_at', 'notes')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def attendance_type_badge(self, obj):
        colors = {
            'IN': '#28a745',
            'OUT': '#dc3545',
            'BREAK_START': '#ffc107',
            'BREAK_END': '#17a2b8',
        }
        color = colors.get(obj.attendance_type, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_attendance_type_display()
        )
    attendance_type_badge.short_description = 'Type'
    
    def status_badge(self, obj):
        colors = {
            'PENDING': '#ffc107',
            'APPROVED': '#28a745',
            'REJECTED': '#dc3545',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Statut'


@admin.register(WorkSession)
class WorkSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'duration', 'break_duration', 'is_complete_badge']
    list_filter = ['is_complete', 'date', 'user']
    search_fields = ['user__username']
    readonly_fields = ['duration', 'is_complete']
    date_hierarchy = 'date'
    
    def is_complete_badge(self, obj):
        if obj.is_complete:
            return format_html('<span style="color: green;">✓ Complète</span>')
        return format_html('<span style="color: orange;">⚠ En cours</span>')
    is_complete_badge.short_description = 'Statut'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type_badge', 'title', 'is_read_badge', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    readonly_fields = ['created_at', 'read_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Destinataire', {
            'fields': ('user',)
        }),
        ('Contenu', {
            'fields': ('notification_type', 'title', 'message', 'attendance')
        }),
        ('État', {
            'fields': ('is_read', 'read_at', 'created_at')
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def notification_type_badge(self, obj):
        colors = {
            'MISSING_CHECK_IN': '#dc3545',
            'MISSING_CHECK_OUT': '#ffc107',
            'LATE_CHECK_IN': '#fd7e14',
            'EARLY_CHECK_OUT': '#20c997',
            'VALIDATION_REQUIRED': '#17a2b8',
            'VALIDATION_APPROVED': '#28a745',
            'VALIDATION_REJECTED': '#dc3545',
        }
        color = colors.get(obj.notification_type, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_notification_type_display()
        )
    notification_type_badge.short_description = 'Type'
    
    def is_read_badge(self, obj):
        if obj.is_read:
            return format_html('<span style="color: green;">✓ Lu</span>')
        return format_html('<span style="color: red; font-weight: bold;">● Non lu</span>')
    is_read_badge.short_description = 'Statut'
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} notification(s) marquée(s) comme lue(s).')
    mark_as_read.short_description = 'Marquer comme lu'
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False, read_at=None)
        self.message_user(request, f'{updated} notification(s) marquée(s) comme non lue(s).')
    mark_as_unread.short_description = 'Marquer comme non lu'


@admin.register(AttendanceSettings)
class AttendanceSettingsAdmin(admin.ModelAdmin):
    list_display = ['get_owner', 'expected_check_in_time', 'expected_check_out_time', 'tolerance_minutes']
    list_filter = ['notify_missing_check_in', 'notify_missing_check_out', 'notify_manager']
    search_fields = ['user__username', 'team__name']
    
    fieldsets = (
        ('Propriétaire', {
            'fields': ('user', 'team'),
            'description': 'Définir les paramètres pour un utilisateur ou une équipe'
        }),
        ('Horaires', {
            'fields': ('expected_check_in_time', 'expected_check_out_time', 'tolerance_minutes')
        }),
        ('Notifications', {
            'fields': ('notify_missing_check_in', 'notify_missing_check_out', 'notify_manager')
        }),
    )
    
    def get_owner(self, obj):
        if obj.user:
            return f"👤 {obj.user.username}"
        elif obj.team:
            return f"👥 {obj.team.name}"
        return "N/A"
    get_owner.short_description = 'Propriétaire'
