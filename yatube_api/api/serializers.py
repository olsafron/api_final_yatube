from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser

from django.forms import ValidationError
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Follow, Post, Group

User: type[AbstractBaseUser] = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Post
        fields: str = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'created', 'post')
        read_only_fields = ('post',)


class GroupSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Follow
        fields = ('following', 'user')

    def validate(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None

        following = validated_data.get('following')
        error_messages = {
            'self_follow': 'Невозможно оформить подписку на самого себя.',
            'already_followed': 'Вы уже подписаны на этого пользователя.',
        }
        error_key = None
        if user == following:
            error_key = 'self_follow'
        elif Follow.objects.filter(user=user, following=following).exists():
            error_key = 'already_followed'
        if error_key:
            raise ValidationError({'detail': error_messages[error_key]})

        return validated_data
