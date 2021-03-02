from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Message
from itertools import chain
from .serializer import MessageSerializer
from  users.serializers import UserSerializer

from rest_framework.response import Response
from rest_framework import status

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @action(detail=False, methods=['get'], url_name='message_list', url_path='message/(?P<receiver_id>\d+)')
    def message_list(self, request, **kwargs):
        messages=list(chain([*Message.objects.filter(sender_id=request.user), *Message.objects.filter(receiver_id=request.user)]))
        serializer = MessageSerializer(messages, many=True, context={'host': request.get_host()})
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_name='message_list', url_path='list/(?P<receiver_id>\d+)')
    def list_Chat_Users(self, request, **kwargs):

        messages = (Message.objects.filter(sender_id=request.user.id) | Message.objects.filter(
            receiver_id=kwargs.get('receiver_id'))).order_by('-timestamp').distinct()
        serializer = MessageSerializer(messages, many=True, context={'host': request.get_host()})
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


    @action(detail=False, methods=['post'], url_name='send_message', url_path='message')
    def send_message(self, request):
        serializer = MessageSerializer(data=request.data, context={'host': request.get_host()})
        if serializer.is_valid():
            serializer.save(receiver=User.objects.get(id=request.data['receiver']), sender=User.objects.get(id=request.data['sender']))
            return JsonResponse(serializer.data, status=201)
        else:
            print(serializer.errors)
        return JsonResponse(serializer.errors, status=400)


    @action(detail=False, methods=['get'], url_name='chat', url_path='chat/(?P<receiver_id>\d+)')
    def chat(self, request, **kwargs):
        sender_data = request.user
        sender = UserSerializer(sender_data, context={'host': request.get_host()}).data
        receivers_data = User.objects.get(id=kwargs.get('receiver_id'))
        receiver = UserSerializer(receivers_data, context={'host': request.get_host()}).data
        messages = (Message.objects.filter(sender=sender_data, receiver=receivers_data) | Message.objects.filter(
            sender=receivers_data, receiver=sender_data)).order_by('timestamp')
        messages_data = MessageSerializer(messages, many=True, context={'host': request.get_host()}).data
        data = {
            'sender': sender,
            'receiver': receiver,
            'messages': messages_data
        }
        return Response(data=data)

