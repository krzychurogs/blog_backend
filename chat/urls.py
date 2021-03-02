from django.urls import path, re_path
from rest_framework import routers
from .import views
from django.urls import path,include

router = routers.DefaultRouter()

router.register('message', views.ChatViewSet)
urlpatterns = [
    path('', include(router.urls)),
]