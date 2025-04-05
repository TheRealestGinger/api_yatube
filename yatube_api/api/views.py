from rest_framework import viewsets

from posts.models import Comment, Group, Post
from .permissions import OwnerOrReadOnly
from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet для постов."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (OwnerOrReadOnly,)

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
    permission_classes = (OwnerOrReadOnly,)

    def get_queryset(self):
        return Post.objects.get(id=self.kwargs.get('post_id')).comments.all()

    def perform_create(self, serializer):
        """Добавляет автора к комментарию."""
        serializer.save(
            author=self.request.user,
            post_id=Post.objects.get(id=self.kwargs.get('post_id')).id
        )
