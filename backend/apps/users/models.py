from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Modèle utilisateur personnalisé pour HoraBadge"""
    
    # Choix de rôles
    ROLE_CHOICES = [
        ('employee', 'Employé'),
        ('manager', 'Manager'),
        ('admin', 'Administrateur'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='employee',
        verbose_name='Rôle'
    )
    function = models.CharField(max_length=50, blank=True, verbose_name='Fonction')
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name='Téléphone')
    
    class Meta:
        db_table = 'users'
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else self.username
    
    @property
    def is_employee(self):
        """Vérifie si l'utilisateur est un employé"""
        return self.role == 'employee'
    
    @property
    def is_manager(self):
        """Vérifie si l'utilisateur est un manager"""
        return self.role == 'manager'
    
    @property
    def is_administrator(self):
        """Vérifie si l'utilisateur est un administrateur"""
        return self.role == 'admin' or self.is_superuser


class Team(models.Model):
    """Modèle pour les équipes"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(User, related_name='teams', blank=True)
    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_teams',
        verbose_name='Responsable'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'teams'
        verbose_name = 'Équipe'
        verbose_name_plural = 'Équipes'
        ordering = ['name']
    
    def __str__(self):
        return self.name