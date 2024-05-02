# Вью.
from django.shortcuts import get_object_or_404

from rest_framework.viewsets import (
    ModelViewSet,
    ReadOnlyModelViewSet,
    GenericViewSet,
)
from rest_framework.filters import SearchFilter
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)

from .pagination import CustomLimitOffsetPagination
from posts.models import Post, Group
from .serializers import (
    FollowSerializer,
    PostSerializer,
    GroupSerializer,
    CommentSerializer,
)
from .permissions import IsOwnerOrReadOnly


class PostViewSet(ModelViewSet):
    """
    CRUD операций с моделью Post.

    Основные атрибуты:
        queryset -- запрос для извлечения объектов Post из базы данных.
        serializer_class -- класс сериализатора объектов Post.
        pagination_class -- класс для пагинации списка объектов Post.
        permission_classes -- клас определения прав доступа к операциям CRUD.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = CustomLimitOffsetPagination
    permission_classes = (
        IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly,
    )

    def perform_create(self, serializer) -> None:
        """Текущий пользователь равен автору."""
        serializer.save(author=self.request.user)


class GroupViewSet(ReadOnlyModelViewSet):
    """
    Класс для представления операций только чтения с моделью Group.

    Основные атрибуты:
        queryset -- запрос для извлечения объектов Group из базы данных.
        serializer_class -- класс сериализатора объектов Group.
        permission_classes -- определеине прав доступа к операциям чтения.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,
    )


class CommentViewSet(ModelViewSet):
    """
    Класс для представления операций CRUD с моделью Comment.

    Основные атрибуты:
        serializer_class -- класс сериализатора объектов Comment.
        permission_classes -- класс определения прав доступа к операциям CRUD.
        pagination_class -- класс для пагинации списка объектов Comment.
    """

    serializer_class = CommentSerializer
    permission_classes = (
        IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly,
    )

    def get_post(self) -> Post:
        """Получить пост или вернуть ошибку 404."""
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, pk=post_id)

    def get_queryset(self):
        """Получить QuerySet комментариев для поста."""
        post: Post = self.get_post()
        return post.comments.all()

    def perform_create(self, serializer) -> None:
        """Текущий пользователь равен автору."""
        post: Post = self.get_post()
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(GenericViewSet, CreateModelMixin, ListModelMixin):
    """
    Класс для представления операций создания и просмотра подписок.

    Основные атрибуты:
        queryset -- запрос для извлечения объектов Follow из базы данных.
        serializer_class -- класс сериализатора объектов Follow.
        permission_classes -- класс для определения прав доступа к операциям.
        pagination_class -- класс для пагинации списка объектов Follow.
        filter_backends -- классы для фильтрации списка объектов Follow.
        search_fields -- поля, по которым осуществляется поиск.
    """

    serializer_class = FollowSerializer
    permission_classes = (
        IsAuthenticated,
    )
    filter_backends = (SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        """Пользователи могут видеть только свои подписки."""
        user = self.request.user
        return user.followers.all()  # Simplified using related_name

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
