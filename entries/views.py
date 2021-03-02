from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Entries,Comments
from .serializers import entriesSerializer,commentsSerializer,entriesInputSerializer
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
        totallik=entries.total_likes();
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
        serializer = entriesInputSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        obj = serializer.save()
        obj.image = image
        obj.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False, url_name='createcomment', url_path=r'createcomment')
    def create_comment(self, request):
        serializer = commentsSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        obj = serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=False, url_name='comments', url_path=r'showcomment/(?P<id>\d+)')
    def comment_list(self, request, **kwargs):
        postid = kwargs.get('id')
        comments = Comments.objects.filter(post=postid)
        serializer = commentsSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_name='posts', url_path=r'showuser/(?P<id>\d+)')
    def post_user_list(self, request, **kwargs):
        entry_author = kwargs.get('id')
        entries = Entries.objects.filter(entry_author=entry_author).order_by('-entry_date')
        serializer = entriesSerializer(entries, many=True,context={'request':request})
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_name='posts', url_path=r'showdetail/(?P<id>\d+)')
    def post_user_detail(self, request, **kwargs):
        id = kwargs.get('id')
        entries = Entries.objects.filter(id=id).order_by('-entry_date')
        serializer = entriesSerializer(entries, many=True, context={'request': request})
        return Response(serializer.data)



    @action(methods=['get'], detail=False, url_name='userposts', url_path=r'allblog')
    def all_blog_list(self, request, **kwargs):
        entries = Entries.objects.raw('SELECT * FROM entries_Entries group by entry_author_id ;')
        serializer = entriesSerializer(entries, many=True)
        return Response(serializer.data)

    @action(methods=['delete'], detail=False, url_name='delete', url_path=r'delete/(?P<id>\d+)')
    def delete_post(self, request, **kwargs):
        post = get_object_or_404(Entries, id=kwargs.get('id'))
        self.check_object_permissions(request, post)
        post.delete()
        return Response(data={'message': 'Pomyślnie usunięto'})


    @action(methods=['patch'], detail=False, url_name='like',url_path=r'like/(?P<id>\d+)/(?P<userid>\d+)')
    def like_add(self, request, **kwargs):
        post = Entries.objects.get(id=kwargs.get('id'))
        self.check_object_permissions(request, post)
        user=kwargs.get('userid');
        is_liked = False
        if post.likes.filter(id=user).exists():
            post.likes.remove(user)
            is_liked = False
        else:
            post.likes.add(user)
            is_liked = True
        serializer = entriesSerializer(post, request.data, context={"host": request.get_host()}, partial=True)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(serializer.data)

