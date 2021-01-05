from django.db import models
from device.models import Device
import uuid

class Stream(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length = 100, unique = False)
    description = models.CharField(max_length = 500, unique = False)
    unit = models.CharField(max_length = 20, unique = False)
    id_device = models.ForeignKey(Device, on_delete=models.CASCADE)

    def create(self, validated_data):
        return Stream.objects.create(**validated_data)