from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from posts.models import Comment, Group, Post
from .permissions import IsAuthenticatedOrOwner
from .serializers import CommentSerializer, GroupSerializer, PostSerializer


def get_post(id):
    return get_object_or_404(Post, id=id)


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet для постов."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrOwner,)

    def perform_create(self, serializer):
        """Добавляет автора к посту."""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для групп."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для комментариев."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrOwner,)

    def get_queryset(self):
        return get_post(self.kwargs.get('post_id')).comments.all()

    def perform_create(self, serializer):
        """Добавляет автора к комментарию."""
        serializer.save(
            author=self.request.user,
            post=get_post(self.kwargs.get('post_id'))
        )
