from rest_framework import serializers
from .models import Stream

# show all streas details
class StreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream
        fields = ['id', 'name', 'description', 'unit', 'id_device']