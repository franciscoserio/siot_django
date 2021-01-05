from django.db import models
from authentication.models import Account
import uuid

class Tenant(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length = 100, unique = False)
    description = models.CharField(max_length = 500, unique = False)

    def create(self, validated_data):
        return Tenant.objects.create(**validated_data)

class UserTenant(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    id_tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    id_user = models.ForeignKey(Account, on_delete=models.CASCADE)
    create_permission = models.BooleanField(default = False)
    read_permission = models.BooleanField(default = False)
    update_permission = models.BooleanField(default = False)
    delete_permission = models.BooleanField(default = False)

    def create(self, validated_data):
        return UserTenant.objects.create(**validated_data)