# Generated by Django 3.1.5 on 2021-02-03 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0007_auto_20210203_1519'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entries',
            name='comments',
        ),
    ]
