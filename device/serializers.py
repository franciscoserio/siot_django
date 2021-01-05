from rest_framework import serializers
from .models import Device

# show all device details
class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'secret', 'name', 'description', 'latitude', 'longitude', 'is_active', 'id_group']

class DeviceListGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'name', 'description', 'latitude', 'longitude', 'is_active']