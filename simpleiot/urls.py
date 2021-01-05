from django.urls import include, path
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

# views
from authentication.views import SignUpView, AddUserView
from group.views import GroupView
from device.views import DeviceView, IndividualDeviceView
from stream.views import StreamView
from tenant.views import AddTenantView

urlpatterns = [
    # authentication
    path('api/admin/authentication', obtain_jwt_token),

    # users
    path('api/signup', SignUpView.as_view()),
    path('api/users', AddUserView.as_view()),

    # tenants
    path('api/tenants', AddTenantView.as_view()),

    path('api/admin/groups', GroupView.as_view()),
    #path('api/admin/group/<uuid:group_id>', IndividualGroupView.as_view()),

    path('api/admin/devices', DeviceView.as_view()),
    path('api/admin/devices/<str:device_id>', IndividualDeviceView.as_view()),

    path('api/admin/devices/<str:device_id>/streams', StreamView.as_view())
]
