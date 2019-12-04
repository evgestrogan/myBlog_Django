from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class PublishedManager(models.Manager):  # Создание своего менеджера модели
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    object = models.Manager()
    published = PublishedManager()

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    # Поле для построения семантических URL'ов для статей
    # unique_for_date - в формировании уникальных URL'ов будет участвовать дата публикации
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    # related_name - имя обратной связи от User к Post
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    # auto_now_add - поле заполнится автоматически при создании объекта
    updated = models.DateTimeField(auto_now=True)
    # auto_now - поле перезаписывается автоматически при сохранении объекта
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    # choices - ограничевает возможные значения списком STATUS_CHOICES

    class Meta:
        ordering = ('-publish',)

    # Meta - содержит метаданные(напр. порядок сортировки ordering)

    def __str__(self):
        return self.title
    # __str__ - возвращает отображение объекта, понятное человеку
