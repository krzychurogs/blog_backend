from django.contrib.auth.models import User, Group
from .models import UserProfile
from rest_framework import serializers
from django.contrib.auth import authenticate


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['id','username', 'email', 'password',]
        extra_kwargs = {'password': {'write_only': True, 'required': True}}


    def create(self, validate_data):
        user = User.objects.create_user(**validate_data)
        return


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = ['user','avatar']




class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and not user.is_staff:
            return user

        raise serializers.ValidationError("Incorrect Credentials")