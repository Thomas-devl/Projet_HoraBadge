#!/usr/bin/env python
"""
Script pour créer des pointages fictifs pour Jean Jacques
Utilisation: python backend/scripts/create_dummy_attendance.py
"""

import os
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.contrib.auth.models import User
from apps.attendance.models import Attendance

def create_dummy_attendance():
    """Crée des pointages fictifs pour Jean Jacques"""
    
    # Chercher l'utilisateur Jean Jacques
    try:
        user = User.objects.get(first_name='Jean', last_name='Jacques')
        print(f"✓ Utilisateur trouvé: {user.get_full_name()} ({user.username})")
    except User.DoesNotExist:
        print("✗ Utilisateur 'Jean Jacques' non trouvé")
        print("\nUtilisateurs disponibles:")
        for u in User.objects.all():
            print(f"  - {u.get_full_name()} ({u.username})")
        return

    # Supprimer les anciens pointages
    old_count = Attendance.objects.filter(user=user).count()
    Attendance.objects.filter(user=user).delete()
    print(f"✓ {old_count} anciens pointages supprimés")

    # Générer des pointages pour les 30 derniers jours
    today = timezone.now().date()
    attendances_created = 0

    for i in range(30):
        current_date = today - timedelta(days=i)
        
        # Sauter les weekends
        if current_date.weekday() >= 5:  # 5=samedi, 6=dimanche
            continue
        
        # Générer un pointage aléatoire
        # Arrivée entre 8h00 et 9h30
        check_in_hour = 8 + (i % 2)  # 8 ou 9
        check_in_minute = (i * 17) % 60  # Varié
        
        # Départ entre 17h00 et 18h30
        check_out_hour = 17 + (i % 2)  # 17 ou 18
        check_out_minute = (i * 23) % 60  # Varié
        
        check_in_time = timezone.make_aware(
            datetime.combine(
                current_date,
                datetime.min.time().replace(hour=check_in_hour, minute=check_in_minute)
            )
        )
        
        check_out_time = timezone.make_aware(
            datetime.combine(
                current_date,
                datetime.min.time().replace(hour=check_out_hour, minute=check_out_minute)
            )
        )
        
        # Créer le pointage
        attendance = Attendance.objects.create(
            user=user,
            check_in=check_in_time,
            check_out=check_out_time
        )
        attendances_created += 1
        
        # Afficher le détail
        hours = (check_out_time - check_in_time).total_seconds() / 3600
        print(f"  {current_date.strftime('%a %d/%m')}: "
              f"{check_in_time.strftime('%H:%M')} → "
              f"{check_out_time.strftime('%H:%M')} "
              f"({hours:.1f}h)")
    
    print(f"\n✓ {attendances_created} pointages créés avec succès!")
    print(f"\nStatistiques:")
    total_hours = sum([
        (a.check_out - a.check_in).total_seconds() / 3600
        for a in Attendance.objects.filter(user=user)
        if a.check_out
    ])
    print(f"  - Total heures: {total_hours:.1f}h")
    print(f"  - Nombre de jours: {attendances_created}")
    print(f"  - Moyenne/jour: {total_hours/attendances_created:.1f}h")

if __name__ == '__main__':
    create_dummy_attendance()
