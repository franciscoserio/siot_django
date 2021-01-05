import uuid
from django.db import models
from tenant.models import Tenant

class Device(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length = 100, unique = True)
    external_id = models.CharField(max_length = 50, unique = False)
    description = models.CharField(max_length = 500, unique = False)
    secret = models.CharField(max_length = 100, unique = True)
    latitude = models.FloatField(default = 0)
    longitude = models.FloatField(default = 0)
    is_active = models.BooleanField(default = True)
    id_tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)

    def create(self, validated_data):
        return Device.objects.create(**validated_data)