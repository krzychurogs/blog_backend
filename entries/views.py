from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Entries
from .serializers import entriesSerializer
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from rest_framework import permissions
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.decorators import action

# Create your views here.
class listPost(APIView):

    def get(self, request):
        entries = Entries.objects.all()
        serializer = entriesSerializer(entries, many=True)
        return Response(serializer.data)

@login_required(login_url='/login')
def like_post(request):
    post = get_object_or_404(Entries, id=request.POST.get('post_id'))
    idpostu = request.POST.get('post_id')
    is_liked = False

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True

    return HttpResponseRedirect(reverse('entry-detail', args=[idpostu]))


class EntriesViewset(viewsets.ModelViewSet):
    queryset = Entries.objects.all().order_by('-entry_date')
    serializer_class = entriesSerializer
    permission_classes = [permissions.AllowAny]

    @action(methods=['post'], detail=False, url_name='create', url_path=r'create')
    def create_post(self, request):
        request.data.pop('image')
        image = request.FILES.get('image', None)
        serializer = entriesSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        obj = serializer.save()
        obj.image = image
        obj.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=False, url_name='posts', url_path=r'showuser/(?P<id>\d+)')
    def post_user_list(self, request, **kwargs):
        entry_author = kwargs.get('id')
        entries = Entries.objects.filter(entry_author=entry_author).order_by('-entry_date')
        serializer = entriesSerializer(entries, many=True)
        return Response(serializer.data)

    @action(methods=['delete'], detail=False, url_name='delete', url_path=r'delete/(?P<id>\d+)')
    def delete_post(self, request, **kwargs):
        post = get_object_or_404(Entries, id=kwargs.get('id'))
        self.check_object_permissions(request, post)
        post.delete()
        return Response(data={'message': 'Pomyślnie usunięto'})

    @action(methods=['put'], detail=False, url_name='add',
            url_path=r'like/(?P<id>\d+)')
    def like_add(self, request, **kwargs):
        post = Entries.objects.get(id=kwargs.get('id'))
        self.check_object_permissions(request, post)
        entry_author = kwargs.get('id')
        is_liked = False
        if post.likes.filter(id=entry_author).exists():
            post.likes.remove(entry_author)
            is_liked = False
        else:
            post.likes.add(entry_author)
            is_liked = True
        serializer = entriesSerializer(post, request.data, context={"host": request.get_host()}, partial=True)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer.update(post, serializer.validated_data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
