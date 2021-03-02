from django.contrib import admin
from .models import UserProfile
# Register your models here.
from rest_framework.authtoken.admin import TokenAdmin
admin.site.register(UserProfile)
TokenAdmin.raw_id_fields = ['user']