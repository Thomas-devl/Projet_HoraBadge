from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Team


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Configuration de l'admin pour le modèle User"""
    list_display = ['username', 'email', 'first_name', 'last_name', 'function', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'function']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('function', 'phone_number')
        }),
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Configuration de l'admin pour le modèle Team"""
    list_display = ['name', 'manager', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'description']
    filter_horizontal = ['members']
    readonly_fields = ['created_at', 'updated_at']
