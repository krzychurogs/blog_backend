from rest_framework import  serializers
from .models import Entries,Comments
from django.contrib.auth.models import User, Group


class userSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields = ['id', 'username', 'email', 'password']

class entriesSerializer(serializers.ModelSerializer):
    entry_author = userSerializer(read_only=True)
    class Meta:
        model=Entries
        fields=['id','entry_title','entry_author','entry_date','image','entry_text','likes','totalLikes']

class entriesInputSerializer(serializers.ModelSerializer):

    class Meta:
        model=Entries
        fields=['id','entry_title','entry_author','entry_date','image','entry_text']


class commentsSerializer(serializers.ModelSerializer):
    comment_author = userSerializer(read_only=True)
    class Meta:
        model=Comments
        fields=['id','comment_title','comment_text','comment_date','comment_author','post']





