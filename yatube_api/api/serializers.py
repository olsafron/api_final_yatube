from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


from posts.models import Comment, Follow, Post, Group, User


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Post
        fields = (
            'id', 'author', 'text', 'pub_date', 'image', 'group'
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'created', 'post')
        read_only_fields = ('author', 'post')


class GroupSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Follow
        fields = ('following', 'user',)
