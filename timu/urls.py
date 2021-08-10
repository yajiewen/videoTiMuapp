from django.urls import path
from .views import *

urlpatterns = [
    path('addtimu/',add_timu),
    path('gettimu/<str:timuuuid>/',get_timu),
]