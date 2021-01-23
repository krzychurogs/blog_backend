from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

from datetime import datetime
from django_resized import ResizedImageField
from datetime import date


# Create your models here.

def upload_path(instance, filname):
    return '/'.join(['post_image', filname])


class Entries(models.Model):
    entry_title = models.CharField(max_length=50, verbose_name=('tytul'), blank=True)
    entry_text = models.TextField(verbose_name=('tekst'), blank=True)
    entry_date = models.DateTimeField(auto_now_add=True)
    entry_author = models.ForeignKey(User, on_delete=models.CASCADE,blank=True )
    image = models.ImageField(blank=True, null=True, upload_to=upload_path)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    @property
    def totalLikes(self):
        return self.likes.count()

    class Meta:
        verbose_name_plural = "entries"

    def __str__(self):
        return f'{self.entry_title}'
