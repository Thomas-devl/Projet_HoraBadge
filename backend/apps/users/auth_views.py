"""
Vues d'authentification pour l'API
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from apps.users.serializers import UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Connecte un utilisateur avec username/email et password
    Retourne un token d'authentification
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'detail': 'Username et password sont requis'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Authentifier l'utilisateur
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        # Connecter l'utilisateur
        login(request, user)
        
        # Créer ou récupérer le token
        token, created = Token.objects.get_or_create(user=user)
        
        # Sérialiser les données utilisateur
        serializer = UserSerializer(user)
        
        return Response({
            'token': token.key,
            'user': serializer.data,
            'message': 'Connexion réussie'
        }, status=status.HTTP_200_OK)
    else:
        return Response(
            {'detail': 'Identifiants invalides'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Déconnecte l'utilisateur et supprime son token
    """
    try:
        # Supprimer le token de l'utilisateur
        request.user.auth_token.delete()
    except Exception as e:
        pass
    
    # Déconnecter l'utilisateur
    logout(request)
    
    return Response(
        {'message': 'Déconnexion réussie'},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request(request):
    """
    Demande de réinitialisation de mot de passe
    Envoie un email avec un lien de réinitialisation
    """
    email = request.data.get('email')
    
    if not email:
        return Response(
            {'detail': 'Email requis'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # TODO: Implémenter l'envoi d'email
    # Pour l'instant, on retourne juste un succès
    
    return Response(
        {'message': 'Si cet email existe, un lien de réinitialisation a été envoyé'},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request):
    """
    Confirme la réinitialisation du mot de passe
    """
    token = request.data.get('token')
    password = request.data.get('password')
    
    if not token or not password:
        return Response(
            {'detail': 'Token et password requis'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # TODO: Implémenter la logique de réinitialisation
    # Pour l'instant, on retourne juste un succès
    
    return Response(
        {'message': 'Mot de passe réinitialisé avec succès'},
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """
    Retourne les informations de l'utilisateur connecté
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)
