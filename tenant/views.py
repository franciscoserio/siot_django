from django.shortcuts import render
from .models import Tenant, UserTenant
from .serializers import TenantSerializer, UserTenantSerializer
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from django.http import JsonResponse

class AddTenantView(APIView):

    def post(self, request):
        
        try:
            if request.user.is_admin == True:

                # request's body data
                if request.data.get('tenant'):
                    body_data = request.data.get('tenant')
                
                else:
                    return JsonResponse({"error" : "JSON parse error"}, status = 400)

                # check if tenant already exists
                tenants = UserTenant.objects.filter(id_user = request.user.id)
                
                for t in tenants:
                    if t.id_tenant.name == body_data["name"]:
                        return JsonResponse({"error" : "Tenant already exists"}, status = 400)

                # check if data is valid
                serializerTenant = TenantSerializer(data = body_data)
                
                if serializerTenant.is_valid(raise_exception = True):
                    
                    # create user into database
                    serializerTenant.save()

                # create association between user and tenant
                serializerUserTenantBody = {
                    "id_tenant" : serializerTenant.data["id"],
                    "id_user" : request.user.id,
                    "create_permission" : 1,
                    "read_permission" : 1,
                    "update_permission" : 1,
                    "delete_permission" : 1
                }

                serializerUserTenant = UserTenantSerializer(data = serializerUserTenantBody)

                if serializerUserTenant.is_valid(raise_exception = True):
                    
                    # create user-tenant association into database
                    serializerUserTenant.save()

                # API response
                response = {
                    "id" : serializerTenant.data["id"],
                    "name" : serializerTenant.data["name"],
                    "description" : serializerTenant.data["description"]
                }

                return JsonResponse(response, status = 201)
            
            else:
                return JsonResponse({"error" : "User not allowed"}, status = 403)

        except ValidationError as e:
            return JsonResponse(e, status = 400)