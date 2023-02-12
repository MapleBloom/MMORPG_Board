from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from crum import get_current_user
from django.urls import reverse

from .utils import get_text_from_html


class Post(models.Model):
    CATEGORIES = [
        ('TA', 'Танки'),
        ('HL', 'Хилы'),
        ('DD', 'ДД'),
        ('TR', 'Торговцы'),
        ('GM', 'Гилдмастеры'),
        ('QG', 'Квестгиверы'),
        ('SM', 'Кузнецы'),
        ('TN', 'Кожевники'),
        ('PT', 'Зельевары'),
        ('SP', 'Мастера заклинаний'),
    ]

    title = models.CharField('Объявление', max_length=64)
    content = RichTextUploadingField('Содержание')
    category = models.CharField('Категория', max_length=2, choices=CATEGORIES, default='TA')
    time_in = models.DateTimeField(auto_now_add=True)
    preview = models.CharField(max_length=64, blank=True, null=True, default=None)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post', editable=False,
                               blank=True, null=True, default=None)

    def save(self, *args, **kwargs):
        if not self.pk:
            user = get_current_user()
            self.author = user
        self.preview = get_text_from_html(self.content)
        super().save(*args, **kwargs)

    def get_title(self):
        return str(self.title).upper()

    def __str__(self):
        return f'{self.get_title()}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.pk)])

    def date_in(self):
        return self.time_in.date()


class Reply(models.Model):
    STATUSES = [
        ('C', 'Создан'),
        ('A', 'Принят'),
        ('D', 'Отклонен'),
    ]

    text = models.CharField('Отклик', max_length=128)
    status = models.CharField('Статус', max_length=1, choices=STATUSES, default='C')
    time_in = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reply', editable=False,
                             blank=True, null=True, default=None)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reply', editable=False,
                               blank=True, null=True, default=None)

    def save(self, *args, **kwargs):
        if not self.pk:
            user = get_current_user()
            self.author = user
            if kwargs.get('pk') and not self.post:
                pk = int(kwargs['pk'])
                self.post = Post.objects.get(pk=pk)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.text}'

    def date_in(self):
        return self.time_in.date()


class News(models.Model):
    title = models.CharField('Новость', max_length=64)
    text = models.CharField('Текст', max_length=128, default='In progress', help_text='preview_text')
    content = RichTextUploadingField('Содержание')
    time_in = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news', editable=False,
                               blank=True, null=True, default=None)

    def save(self, *args, **kwargs):
        user = get_current_user()
        if not self.pk:
            self.author = user
        super().save(*args, **kwargs)

    def get_title(self):
        return str(self.title).upper()

    def __str__(self):
        return f'{self.get_title()}'

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.pk)])

    def preview(self):
        return f'{self.text[:64]}...'

    def date_in(self):
        return self.time_in.date()
