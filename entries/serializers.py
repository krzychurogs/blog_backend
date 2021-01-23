from rest_framework import  serializers
from .models import Entries


class entriesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Entries
        fields=['id','entry_title','entry_author','entry_date','image','entry_text','likes','totalLikes']