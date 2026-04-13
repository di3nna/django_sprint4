from django.db import models
from django.contrib.auth import get_user_model
import datetime
from django.urls import reverse


class BaseModel(models.Model):
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.')
    created_at = models.DateTimeField(
        'Добавлено',
        auto_now_add=True)

    class Meta:
        abstract = True


User = get_user_model()


class Category(BaseModel):
    title = models.CharField(
        'Заголовок',
        max_length=256,
        blank=False)
    description = models.TextField(
        'Описание',
        blank=False)
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        blank=False,
        help_text='Идентификатор страницы для URL; разрешены символы '
        'латиницы, цифры, дефис и подчёркивание.')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Location(BaseModel):
    name = models.CharField(
        'Название места',
        max_length=256,
        blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'


class Post(BaseModel):
    image = models.ImageField(
        'Изображение',
        upload_to='posts_images/',
        blank=True)
    title = models.CharField(
        'Заголовок',
        max_length=256,
        blank=False)
    text = models.TextField(
        'Текст',
        blank=False)
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        default=datetime.datetime.now,
        blank=False,
        help_text='Если установить дату и время в будущем'
        ' — можно делать отложенные публикации.')
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        related_name='location',
        verbose_name='Местоположение',
        null=True,
        blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='category',
        verbose_name='Категория',
        null=True,
        blank=False)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Автор публикации',
        blank=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.pk})

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-pub_date']


class Comment(models.Model):
    text = models.TextField('Текст комментария')
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
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.author} — {self.text[:20]}'
