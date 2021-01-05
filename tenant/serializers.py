from rest_framework import serializers
from .models import Tenant, UserTenant

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ['id', 'name', 'description']

class UserTenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTenant
        fields = ['id', 'id_tenant', 'id_user', 'create_permission', 'read_permission', 'update_permission', 'delete_permission']