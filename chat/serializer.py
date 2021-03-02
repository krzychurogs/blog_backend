from rest_framework import serializers

from .models import Message

from users.serializers import UserSerializer,UserProfileSerializer
class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField('get_sender')
    receiver = serializers.SerializerMethodField('get_receiver')

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'timestamp']

    def get_sender(self, instance):
        return UserSerializer(instance.sender, context=self.context).data

    def get_receiver(self, instance):
        return UserSerializer(instance.receiver, context=self.context).data