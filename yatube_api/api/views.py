from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from posts.models import Comment, Group, Post
from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet для постов."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        """Добавляет автора к посту."""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Обновляет пост."""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого поста запрещено!')
        serializer.save()

    def perform_destroy(self, instance):
        """Удаляет пост."""
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого поста запрещено!')
        instance.delete()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для групп."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для комментариев."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        """Возвращает комментарии к посту, заменяя id автора на имя."""
        return super().get_queryset().filter(
            post_id=self.kwargs.get('post_id')
        )

    def perform_create(self, serializer):
        """Добавляет автора к комментарию."""
        serializer.save(
            author=self.request.user,
            post_id=self.kwargs.get('post_id')
        )

    def perform_update(self, serializer):
        """Обновляет комментарий."""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого комментария запрещено!')
        serializer.save(
            post_id=self.kwargs.get('post_id')
        )

    def perform_destroy(self, instance):
        """Удаляет комментарий."""
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого комментария запрещено!')
        instance.delete()
