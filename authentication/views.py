#from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework import permissions
from authentication.serializers import UserSerializer
from rest_framework.renderers import JSONRenderer
from tenant.models import Tenant, UserTenant
#from group.serializers import GroupLoginSerializer
from .serializers import UserSignUpSerializer, UserAddSerializer
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.views import exception_handler
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password

def jwt_response_payload_handler(token, email=None, request=None):
    
    # user data
    user_data = UserSerializer(email,context={'request': request}).data

    # get tenants
    tenants = UserTenant.objects.filter(id_user = user_data["id"])

    # tenants and permissions
    tenants_and_permissions = []

    for t in tenants:
        aux_dict = {
            "name" : t.id_tenant.name,
            "permissions" : []
        }
        
        if t.create_permission == True:
            aux_dict['permissions'].append('Create')
        
        if t.read_permission == True:
            aux_dict['permissions'].append('Read')
        
        if t.update_permission == True:
            aux_dict['permissions'].append('Update')
        
        if t.delete_permission == True:
            aux_dict['permissions'].append('Delete')

        tenants_and_permissions.append(aux_dict)

    return {
        'token': token,
        'user': UserSerializer(email,context={'request': request}).data,
        'tenants' : tenants_and_permissions
    }

# get and create
@authentication_classes([])
@permission_classes([])
class SignUpView(APIView):

    def post(self, request):
        
        try:
            
            # request's body data
            if request.data.get('user'):
                body_data = request.data.get('user')
                body_data["password"] = make_password(body_data["password"])

            else:
                return JsonResponse({"error" : "JSON parse error"}, status = 400)

            # check if data is valid
            serializer = UserSignUpSerializer(data = body_data)
            
            if serializer.is_valid(raise_exception = True):
                
                # create user into database
                device_saved = serializer.save()

            response = {
                "id" : serializer.data["id"],
                "email" : serializer.data["email"],
                "first_name" : serializer.data["first_name"],
                "last_name" : serializer.data["last_name"]
            }

            return JsonResponse(response, status = 201)

        except ValidationError as e:
            return JsonResponse(e, status = 400)

class AddUserView(APIView):

    def post(self, request):
        
        try:
            if request.user.is_admin == True:

                # request's body data
                if request.data.get('user'):
                    body_data = request.data.get('user')
                    body_data["password"] = make_password(body_data["password"])
                    body_data['is_admin'] = False
                    body_data['admin_id'] = request.user.id
                
                else:
                    return JsonResponse({"error" : "JSON parse error"}, status = 400)

                # check if data is valid
                serializer = UserAddSerializer(data = body_data)
                
                if serializer.is_valid(raise_exception = True):
                    
                    # create user into database
                    serializer.save()

                response = {
                    "id" : serializer.data["id"],
                    "email" : serializer.data["email"],
                    "first_name" : serializer.data["first_name"],
                    "last_name" : serializer.data["last_name"]
                }

                return JsonResponse(response, status = 201)
            
            else:
                return JsonResponse({"error" : "User not allowed"}, status = 403)

        except ValidationError as e:
            return JsonResponse(e, status = 400)