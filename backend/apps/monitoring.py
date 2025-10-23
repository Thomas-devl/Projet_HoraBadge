"""
Health Check Views - Monitoring du Backend
Fournit des endpoints pour vérifier l'état de santé du système
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import get_resolver, URLPattern, URLResolver
from datetime import datetime, timedelta
import sys
import time

User = get_user_model()


class HealthCheckView(APIView):
    """
    GET /api/health/ - Health check complet du système
    Accessible sans authentification pour monitoring externe
    """
    permission_classes = []  # Pas d'authentification requise
    
    def get(self, request):
        """Vérifier l'état de santé de tous les composants"""
        
        health_status = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'components': {}
        }
        
        # 1. Base de données
        db_health = self._check_database()
        health_status['components']['database'] = db_health
        
        # 2. Modèles Django
        models_health = self._check_models()
        health_status['components']['models'] = models_health
        
        # 3. Routes API - Teste TOUTES les routes
        routes_health = self._check_all_routes()
        health_status['components']['routes'] = routes_health
        
        # 4. Tests des endpoints critiques
        endpoints_health = self._check_critical_endpoints()
        health_status['components']['endpoints'] = endpoints_health
        
        # 5. Cache (si configuré)
        cache_health = self._check_cache()
        health_status['components']['cache'] = cache_health
        
        # Déterminer le statut global
        all_healthy = all(
            comp['status'] == 'healthy' 
            for comp in health_status['components'].values()
        )
        
        health_status['status'] = 'healthy' if all_healthy else 'degraded'
        
        # Retourner 200 si healthy, 503 si degraded
        response_status = status.HTTP_200_OK if all_healthy else status.HTTP_503_SERVICE_UNAVAILABLE
        
        return Response(health_status, status=response_status)
    
    def _check_database(self):
        """Vérifier la connexion à la base de données"""
        try:
            # Tester la connexion
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            
            # Compter les tables
            tables = connection.introspection.table_names()
            
            # Compter les utilisateurs
            user_count = User.objects.count()
            
            return {
                'status': 'healthy',
                'type': settings.DATABASES['default']['ENGINE'].split('.')[-1],
                'tables_count': len(tables),
                'users_count': user_count,
                'message': '✅ Base de données opérationnelle'
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e),
                'message': '❌ Erreur de connexion à la base de données'
            }
    
    def _check_models(self):
        """Vérifier les modèles Django"""
        try:
            from apps.users.models import Team
            from apps.attendance.models import Attendance, WorkSession, Notification
            
            models_stats = {
                'users': User.objects.count(),
                'teams': Team.objects.count(),
                'attendances': Attendance.objects.count(),
                'work_sessions': WorkSession.objects.count(),
                'notifications': Notification.objects.count(),
            }
            
            return {
                'status': 'healthy',
                'models': models_stats,
                'message': '✅ Tous les modèles accessibles'
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e),
                'message': '❌ Erreur dans les modèles'
            }
    
    def _check_all_routes(self):
        """Lister et vérifier TOUTES les routes de l'application"""
        try:
            resolver = get_resolver()
            
            def extract_routes(patterns, prefix=''):
                routes = []
                for pattern in patterns:
                    if isinstance(pattern, URLResolver):
                        # C'est un include(), explorer récursivement
                        new_prefix = prefix + str(pattern.pattern)
                        routes.extend(extract_routes(pattern.url_patterns, new_prefix))
                    elif isinstance(pattern, URLPattern):
                        # C'est une route finale
                        route = prefix + str(pattern.pattern)
                        routes.append({
                            'path': route,
                            'name': pattern.name or 'unnamed',
                            'view': pattern.callback.__name__ if hasattr(pattern.callback, '__name__') else str(pattern.callback)
                        })
                return routes
            
            all_routes = extract_routes(resolver.url_patterns)
            
            # Organiser par catégorie
            api_routes = [r for r in all_routes if 'api/' in r['path']]
            admin_routes = [r for r in all_routes if 'admin/' in r['path']]
            other_routes = [r for r in all_routes if 'api/' not in r['path'] and 'admin/' not in r['path']]
            
            # Routes critiques attendues
            critical_paths = [
                'api/users/',
                'api/teams/',
                'api/attendance/',
                'api/clocks/',
                'api/reports/',
                'api/health/',
            ]
            
            missing_critical = []
            found_critical = []
            
            for critical in critical_paths:
                found = any(critical in route['path'] for route in all_routes)
                if found:
                    found_critical.append(critical)
                else:
                    missing_critical.append(critical)
            
            all_critical_found = len(missing_critical) == 0
            
            return {
                'status': 'healthy' if all_critical_found else 'degraded',
                'total_routes': len(all_routes),
                'api_routes': len(api_routes),
                'admin_routes': len(admin_routes),
                'other_routes': len(other_routes),
                'critical_routes_found': len(found_critical),
                'critical_routes_missing': missing_critical if missing_critical else None,
                'routes_list': {
                    'api': [r['path'] for r in api_routes[:20]],  # Limiter à 20 pour affichage
                    'admin': [r['path'] for r in admin_routes[:10]],
                    'other': [r['path'] for r in other_routes[:10]],
                },
                'message': '✅ Toutes les routes critiques présentes' if all_critical_found else f'⚠️ Routes manquantes: {", ".join(missing_critical)}'
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e),
                'message': '❌ Erreur lors de l\'analyse des routes'
            }
    
    def _check_critical_endpoints(self):
        """Tester les endpoints API critiques"""
        try:
            from django.test import Client
            
            client = Client()
            endpoints = []
            
            # Liste des endpoints à tester
            tests = [
                {'url': '/api/users/', 'method': 'get', 'name': 'Liste utilisateurs'},
                {'url': '/api/teams/', 'method': 'get', 'name': 'Liste équipes'},
                {'url': '/api/attendance/', 'method': 'get', 'name': 'Liste pointages'},
                {'url': '/api/reports/', 'method': 'get', 'name': 'Rapports globaux'},
                {'url': '/api/health/quick/', 'method': 'get', 'name': 'Health check rapide'},
                {'url': '/admin/', 'method': 'get', 'name': 'Admin Django'},
            ]
            
            total_ok = 0
            total_failed = 0
            
            for test in tests:
                start_time = time.time()
                try:
                    if test['method'] == 'get':
                        response = client.get(test['url'])
                    
                    response_time = round((time.time() - start_time) * 1000, 2)  # en ms
                    
                    # Considérer OK si status < 500 (même 403 est OK, c'est juste l'auth)
                    is_ok = response.status_code < 500
                    
                    if is_ok:
                        total_ok += 1
                    else:
                        total_failed += 1
                    
                    endpoints.append({
                        'name': test['name'],
                        'url': test['url'],
                        'status_code': response.status_code,
                        'response_time_ms': response_time,
                        'status': 'ok' if is_ok else 'error'
                    })
                except Exception as e:
                    total_failed += 1
                    endpoints.append({
                        'name': test['name'],
                        'url': test['url'],
                        'error': str(e),
                        'status': 'error'
                    })
            
            all_ok = total_failed == 0
            
            return {
                'status': 'healthy' if all_ok else 'degraded',
                'total_tested': len(tests),
                'total_ok': total_ok,
                'total_failed': total_failed,
                'endpoints': endpoints,
                'message': f'✅ {total_ok}/{len(tests)} endpoints fonctionnels' if all_ok else f'⚠️ {total_failed} endpoint(s) en erreur'
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e),
                'message': '❌ Impossible de tester les endpoints'
            }
    

    
    def _check_cache(self):
        """Vérifier le cache Django"""
        try:
            # Tester le cache
            test_key = 'health_check_test'
            test_value = 'ok'
            
            cache.set(test_key, test_value, 10)
            retrieved = cache.get(test_key)
            cache.delete(test_key)
            
            cache_works = retrieved == test_value
            
            return {
                'status': 'healthy' if cache_works else 'degraded',
                'message': '✅ Cache opérationnel' if cache_works else '⚠️ Cache non fonctionnel'
            }
        except Exception as e:
            return {
                'status': 'degraded',
                'error': str(e),
                'message': '⚠️ Cache non configuré ou en erreur'
            }


class DetailedStatsView(APIView):
    """
    GET /api/health/stats/ - Statistiques détaillées du système
    Nécessite authentification admin
    """
    
    def get(self, request):
        """Statistiques complètes du système"""
        from apps.attendance.models import Attendance, WorkSession, Notification
        from apps.users.models import Team
        from django.utils import timezone
        
        now = timezone.now()
        today = now.date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        stats = {
            'timestamp': now.isoformat(),
            'database': {
                'total_users': User.objects.count(),
                'active_users': User.objects.filter(is_active=True).count(),
                'staff_users': User.objects.filter(is_staff=True).count(),
                'total_teams': Team.objects.count(),
            },
            'attendance': {
                'total_attendances': Attendance.objects.count(),
                'today': Attendance.objects.filter(date=today).count(),
                'this_week': Attendance.objects.filter(date__gte=week_ago).count(),
                'this_month': Attendance.objects.filter(date__gte=month_ago).count(),
            },
            'work_sessions': {
                'total': WorkSession.objects.count(),
                'this_week': WorkSession.objects.filter(check_in__date__gte=week_ago).count(),
            },
            'notifications': {
                'total': Notification.objects.count(),
                'unread': Notification.objects.filter(is_read=False).count(),
            },
            'system': {
                'python_version': sys.version,
                'django_version': settings.VERSION if hasattr(settings, 'VERSION') else 'Unknown',
                'debug_mode': settings.DEBUG,
            }
        }
        
        return Response(stats)


class QuickHealthView(APIView):
    """
    GET /api/health/quick/ - Health check rapide (juste DB)
    Pour monitoring externe fréquent
    """
    permission_classes = []
    
    def get(self, request):
        """Health check ultra-rapide"""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            return Response({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat()
            })
        except Exception as e:
            return Response({
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
