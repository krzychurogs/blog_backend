# Generated by Django 3.1.5 on 2021-02-04 20:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('entries', '0016_auto_20210204_2048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='comment_author',
        ),
        migrations.AddField(
            model_name='comments',
            name='comment_author',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
