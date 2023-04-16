from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from posts.models import Post, Group, Follow
from .serializers import CommentSerializer, PostSerializer, GroupSerializer,\
    FollowSerializer


class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def is_author(self, item):
        if isinstance(item, PostSerializer):
            if item.instance.author != self.request.user:
                raise PermissionDenied('Изменение чужого контента запрещено!')
            return True
        elif isinstance(item, Post):
            if item.author != self.request.user:
                raise PermissionDenied('Изменение чужого контента запрещено!')
            return True
        return False

    def perform_update(self, serializer):
        self.is_author(serializer)
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        self.is_author(instance)
        instance.delete()


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer

    def get_post(self, ):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post

    def perform_create(self, serializer):
        post = self.get_post()
        serializer.save(author=self.request.user,
                        post=post)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        instance.delete()

    def get_queryset(self):
        post = self.get_post()
        return post.comments.all()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def perform_create(self, serializer):
        if serializer.instance.author == 'admin':
            post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
            serializer.save(author=self.request.user, post=post)
        return Response(status=405)

    def perform_update(self, serializer):
        if serializer.instance.author == 'admin':
            if serializer.instance.author != self.request.user:
                raise PermissionDenied('Изменение чужого контента запрещено!')
            super(GroupViewSet, self).perform_update(serializer)
        return Response(status=405)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('user__username', 'following__username')

    def get_queryset(self):
        queryset = Follow.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        if serializer.validated_data['following'] != self.request.user:
            serializer.save(user=self.request.user)
        else:
            return Response(status=400)
