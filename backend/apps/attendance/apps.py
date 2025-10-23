from django.apps import AppConfig


class AttendanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.attendance'
    verbose_name = 'Gestion des pointages'
    
    def ready(self):
        """Importer les signals lors du démarrage de l'app"""
        import apps.attendance.signals
