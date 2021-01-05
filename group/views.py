from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Group
from .serializers import GroupSerializer
import json

class GroupView(APIView):

    def get(self, request):
        # get groups related to the authenticated user
        groups = Group.objects.all().filter(id_user = request.user.id)
        serializer = GroupSerializer(groups, many=True)
        return Response({"groups": serializer.data})

    def post(self, request):
        # request's body data
        body_data = request.data.get('group')

        # check if data is valid
        serializer = GroupSerializer(data = body_data)

        if serializer.is_valid(raise_exception=True):

            # create group into database
            group_saved = serializer.save()

        return Response(serializer.data, status = status.HTTP_201_CREATED)