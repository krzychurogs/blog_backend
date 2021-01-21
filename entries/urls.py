"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from .models import Entries
from .import views
from django.conf.urls import url
from .views import listPost,DeleteView,\
    like_post
router = routers.DefaultRouter()
router.register('posthandle', views.EntriesViewset)

urlpatterns = [
    path('', include(router.urls)),
    url(r'like/$',like_post,name="like_post"),
    url(r'^posty/',listPost.as_view()),
    path('messages/', include('chat.urls')),
    ]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
