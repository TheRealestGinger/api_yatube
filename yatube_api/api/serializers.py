from rest_framework import serializers

from posts.models import Post, Group, Comment


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для постов."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Post
        fields = ('text', 'image', 'group', 'id', 'author', 'pub_date')
        read_only_fields = ('id', 'pub_date')


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для групп."""

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')
        read_only_fields = ('id', 'title', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('text', 'id', 'author', 'post', 'created')
        read_only_fields = ('id', 'post', 'created')
