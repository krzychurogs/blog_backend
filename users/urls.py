from django.urls import path,include
from .import views
from knox import views as knox_views
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CustomAuthToken,LoginAPIView
from rest_framework import routers
from rest_framework.authtoken.views import  ObtainAuthToken
from django.contrib.auth import views as auth_views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('profile/', views.ProfileView.as_view()),
    path('auth/', views.CustomAuthToken.as_view()),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
]
format_suffix_patterns(urlpatterns)

