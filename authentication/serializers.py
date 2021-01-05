from rest_framework import serializers
from .models import Account

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'email']

class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'email', 'password', 'first_name', 'last_name']

class UserAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'admin_id', 'is_admin']