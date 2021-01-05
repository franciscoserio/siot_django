import uuid
from django.db import models
from authentication.models import Account

class Group(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length = 100, unique = True)
    description = models.CharField(max_length = 500, unique = False)
    id_user = models.ForeignKey(Account, on_delete=models.CASCADE)

    def create(self, validated_data):
        return Group.objects.create(**validated_data)