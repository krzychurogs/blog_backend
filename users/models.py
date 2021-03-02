from django.db import models
from django.contrib.auth.models import User
# Create your models here.

def upload_path(instance, filname):
    return '/'.join(['post_image', filname])

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True )
    avatar = models.ImageField(blank=True, null=True, upload_to=upload_path)
