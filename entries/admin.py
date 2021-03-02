from django.contrib import admin

# Register your models here.
from .models import Entries,Comments

admin.site.register(Entries)
admin.site.register(Comments)