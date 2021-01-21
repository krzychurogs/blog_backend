from rest_framework import  serializers
from .models import Entries


class entriesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Entries
        fields='__all__'