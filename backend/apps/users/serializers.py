"""
Serializers for users app
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Team

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    
    # Champs en lecture seule calculés
    full_name = serializers.SerializerMethodField()
    team_names = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'role',
            'function',
            'phone_number',
            'is_active',
            'is_staff',
            'team_names',
            'date_joined',
        ]
        read_only_fields = ['id', 'date_joined', 'full_name', 'team_names']
    
    def get_full_name(self, obj):
        """Retourne le nom complet"""
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username
    
    def get_team_names(self, obj):
        """Retourne la liste des équipes"""
        return [team.name for team in obj.teams.all()]


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating users with password"""
    
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password_confirm',
            'first_name',
            'last_name',
            'function',
            'phone_number',
        ]
    
    def validate(self, data):
        """Valider que les mots de passe correspondent"""
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': "Les mots de passe ne correspondent pas."
            })
        return data
    
    def create(self, validated_data):
        """Créer l'utilisateur avec mot de passe hashé"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Team model"""
    
    # Champs calculés
    manager_username = serializers.CharField(source='manager.username', read_only=True)
    manager_name = serializers.SerializerMethodField()
    member_count = serializers.SerializerMethodField()
    member_usernames = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = [
            'id',
            'name',
            'description',
            'manager',
            'manager_username',
            'manager_name',
            'members',
            'member_usernames',
            'member_count',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'manager_username', 'manager_name', 'member_count', 'member_usernames']
    
    def get_manager_name(self, obj):
        """Retourne le nom du manager"""
        if obj.manager:
            return f"{obj.manager.first_name} {obj.manager.last_name}".strip() or obj.manager.username
        return None
    
    def get_member_count(self, obj):
        """Retourne le nombre de membres"""
        return obj.members.count()
    
    def get_member_usernames(self, obj):
        """Retourne la liste des usernames des membres"""
        return [member.username for member in obj.members.all()]


class TeamDetailSerializer(TeamSerializer):
    """Serializer détaillé pour Team avec infos des membres"""
    
    members_detail = UserSerializer(source='members', many=True, read_only=True)
    manager_detail = UserSerializer(source='manager', read_only=True)
    
    class Meta(TeamSerializer.Meta):
        fields = TeamSerializer.Meta.fields + ['members_detail', 'manager_detail']
