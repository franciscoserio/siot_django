from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Stream
from .serializers import StreamSerializer
import json
from django.utils.crypto import get_random_string
from django.shortcuts import render

# get and create 
class StreamView(APIView):

    def get(self, request):

        try:
            # get stream related to the authenticated user
            groups = Group.objects.all().filter(id_user = request.user.id)
            group_serializer = GroupSerializer(groups, many=True)

            resp = {}

            for g in group_serializer.data:

                devices = Device.objects.all().filter(id_group = g['id'])
                device_serializer = DeviceListGroupSerializer(devices, many=True)
                
                resp[g['name']] = device_serializer.data

            return Response(resp)
        
        except Exception as e:
            return Response({"message" : e}, status = 400)

    def post(self, request):

        try:
            # request's body data
            body_data = request.data.get('device')

            # generate a secret
            body_data['secret'] = get_random_string(length = 32)

            # check if data is valid
            serializer = DeviceSerializer(data = body_data)

            if serializer.is_valid(raise_exception = True):

                # create device into database
                device_saved = serializer.save()

            return Response(serializer.data, status = status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"message" : e}, status = 400)

# update and delete
class IndividualDeviceView(APIView):
    
    def get(self, request, device_id):
        
        try:
            devices = Device.objects.all().filter(id = device_id)
            device_serializer = DeviceSerializer(devices, many = True)

            if len(device_serializer.data) > 0:
                return Response(device_serializer.data[0], status = 200)

            else:
                return Response({"message" : "Device not exists"}, status = 400)

        except Exception as e:
            return Response({"message" : e}, status = 400)

    def delete(self, request, device_id):

        try:
            if Device.objects.filter(id = device_id).exists():

                # delete device
                Device.objects.filter(id = device_id).delete()
                return Response({"message" : "Device deleted"}, status = 200)

            else:
                return Response({"message" : "Device not exists"}, status = 400)
        
        except Exception as e:
            return Response({"message" : e}, status = 400)
    
    def put(self, request, device_id):

        try:
            if Device.objects.filter(id = device_id).exists():

                # request's body data
                body_data = request.data.get('device')
                
                # update device
                Device.objects.filter(id = device_id).update(**body_data)

                return Response({"message" : "Device updated"}, status = 200)

            else:
                return Response({"message" : "Device not exists"}, status = 400)
        
        except Exception as e:
            return Response({"message" : e}, status = 400)