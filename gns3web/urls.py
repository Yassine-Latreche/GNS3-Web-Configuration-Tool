"""tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from gns3webadmin import views as gsn3Views
from projects import views as projectViews
from project_main import views as projectMainViews
from device import views as deviceViews
from link import views as linkViews

router = routers.DefaultRouter()
router.register(r'groups', gsn3Views.GroupViewSet)
router.register(r'users', gsn3Views.UserViewSet)
router.register(r'connections', gsn3Views.ConnectionViewSet)


urlpatterns = [
    path('', gsn3Views.index, name='connections'),
    
    path('connections', gsn3Views.connectionList, name='connection-list'),
    path('connections/create', gsn3Views.connectionCreate, name='connection-create'),
    path('connections/<int:id>', gsn3Views.connectionUpdate, name='connection-update'),
    path('connections/<int:id>/delete', gsn3Views.connectionDelete, name='connection-delete'),

    path('connections/<int:connection_id>/projects', projectViews.projectList, name='project-list'),
    path('connections/<int:connection_id>/projects/create', projectViews.projectCreate, name='project-create'),
    path('connections/<int:connection_id>/projects/<str:id>', projectViews.projectUpdate, name='project-update'),
    path('connections/<int:connection_id>/projects/<str:id>/delete', projectViews.projectDelete, name='project-delete'),

    path('connections/<int:connection_id>/projects/<str:project_id>/dashboard', projectMainViews.projectMainDashboard, name='project-main-dashboard'),
    path('connections/<int:connection_id>/projects/<str:project_id>/dashboard/open', projectMainViews.projectMainOpen, name='project-main-open'),
    path('connections/<int:connection_id>/projects/<str:project_id>/dashboard/close', projectMainViews.projectMainClose, name='project-main-close'),
    path('connections/<int:connection_id>/projects/<str:project_id>/dashboard/network', projectMainViews.projectMainNetwork, name='project-main-network'),
    path('connections/<int:connection_id>/projects/<str:project_id>/dashboard/create', projectMainViews.projectMainCreateDevice, name='project-main-create-device'),

    path('connections/<int:connection_id>/projects/<str:project_id>/devices/<str:device_id>/view', deviceViews.deviceIndex, name='device-view'),
    path('connections/<int:connection_id>/projects/<str:project_id>/devices/<str:device_id>/delete', deviceViews.deviceDelete, name='device-delete'),
    
    path('connections/<int:connection_id>/projects/<str:project_id>/devices/<str:device_id>/start', deviceViews.deviceStart, name='device-start'),
    path('connections/<int:connection_id>/projects/<str:project_id>/devices/<str:device_id>/reload', deviceViews.deviceReload, name='device-reload'),
    path('connections/<int:connection_id>/projects/<str:project_id>/devices/<str:device_id>/suspend', deviceViews.deviceSuspend, name='device-suspend'),
    path('connections/<int:connection_id>/projects/<str:project_id>/devices/<str:device_id>/stop', deviceViews.deviceStop, name='device-stop'),
    
    path('connections/<int:connection_id>/projects/<str:project_id>/devices/<str:device_id>/running_config', deviceViews.deviceRunningConfig, name='device-running-config'),
    path('connections/<int:connection_id>/projects/<str:project_id>/devices/<str:device_id>/startup_config', deviceViews.deviceStartupConfig, name='device-startup-config'),
    path('connections/<int:connection_id>/projects/<str:project_id>/devices/<str:device_id>/ip_routes', deviceViews.deviceIpRoute, name='device-ip-routes'),
    path('connections/<int:connection_id>/projects/<str:project_id>/devices/<str:device_id>/ping/<str:ip_address>', deviceViews.devicePingIpAddress, name='device-ping-ip-address'),
    path('connections/<int:connection_id>/projects/<str:project_id>/devices/<str:device_id>/copy_running_to_startup', deviceViews.deviceCopyRunningToStartup, name='device-copy-running-to-startup'),
    path('connections/<int:connection_id>/projects/<str:project_id>/devices/<str:device_id>/vlans', deviceViews.deviceGetVlans, name='device-get-vlans'),
    path('connections/<int:connection_id>/projects/<str:project_id>/devices/<str:device_id>/create_vlan', deviceViews.deviceCreateVlan, name='device-create-vlans'),
    path('connections/<int:connection_id>/projects/<str:project_id>/devices/<str:device_id>/guest_ip_address', deviceViews.deviceGuestIpAddress, name='device-guest-ip-address'),
    path('connections/<int:connection_id>/projects/<str:project_id>/devices/<str:device_id>/vlan_access_mode', deviceViews.deviceVlanAccessMode, name='device-ports-access-mode'),
    path('connections/<int:connection_id>/projects/<str:project_id>/devices/<str:device_id>/interfaces_ip_address', deviceViews.deviceInterfacesIpAddress, name='device-interfaces-ip-address'),
    path('connections/<int:connection_id>/projects/<str:project_id>/devices/<str:device_id>/guest_show_ip', deviceViews.deviceGuestShowIp, name='device-guest-show-ip'),
    path('connections/<int:connection_id>/projects/<str:project_id>/devices/<str:device_id>/add_static_route', deviceViews.deviceAddStaticRoute, name='device-add-static-route'),

    path('connections/<int:connection_id>/projects/<str:project_id>/links', linkViews.linkIndex, name='device-link-index'),
    path('connections/<int:connection_id>/projects/<str:project_id>/links/create', linkViews.linkCreate, name='device-link-create'),
    path('connections/<int:connection_id>/projects/<str:project_id>/links/<str:link_id>/delete', linkViews.deleteLink, name='device-link-delete'),

    # path('connections/<int:connection_id>/projects/<str:id>/dashboard', projectViews.projectCreate, name='project-create'),
    # path('connections/<int:connection_id>/projects/<str:id>/dashboard', projectViews.projectUpdate, name='project-update'),
    # path('connections/<int:connection_id>/projects/<str:id>/dashboard', projectViews.projectDelete, name='project-delete'),
    
    path('admin/', admin.site.urls),
    path("register", gsn3Views.register_request, name="register"),
    path("login", gsn3Views.login_request, name="login"),

    # path('accounts/', include('django.contrib.auth.urls')),

    path('api', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]