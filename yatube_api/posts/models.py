from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

User: type[AbstractBaseUser] = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name='название')
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    description = models.TextField(verbose_name='описание')

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
    )
    image = models.ImageField(
        upload_to='posts/',
        null=True,
        blank=True,
        verbose_name='Изображение'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True,
        null=True,
        verbose_name='Группы'
    )

    def __str__(self) -> str:
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост'
    )
    text = models.TextField(verbose_name='Текст')
    created = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        db_index=True
    )


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='Подписчик',
    )

    class Meta:
        unique_together = ('user', 'following')
        verbose_name: str = ('Подписка')

    def __str__(self) -> str:
        return f'{self.user.username} подписан на {self.following.username}'
