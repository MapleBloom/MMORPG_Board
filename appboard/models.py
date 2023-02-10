from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from crum import get_current_user
from django.urls import reverse


# class Post(models.Model):
#     CATEGORIES = [
#         ('TN', 'Танки'),
#         ('HL', 'Хилы'),
#         ('DD', 'ДД'),
#         ('TR', 'Торговцы'),
#         ('GM', 'Гилдмастеры'),
#         ('QG', 'Квестгиверы'),
#         ('SM', 'Кузнецы'),
#         ('TN', 'Кожевники'),
#         ('PT', 'Зельевары'),
#         ('SP', 'Мастера заклинаний'),
#     ]
#
#     title = models.CharField(max_length=128)
#     text = models.TextField(default='In progress')
#     time_in = models.DateTimeField(auto_now_add=True)
#     category = models.CharField(max_length=2, choices=CATEGORIES, default='NW')
#
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ad')
#
#     def get_title(self):
#         return str(self.title).upper()
#
#     def __str__(self):
#         return f'{self.get_title()}'

    # def get_absolute_url(self):
    #     return reverse('post_detail', args=[str(self.id)])

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     cache.delete(f'post-{self.pk}')

    # def preview(self):
    #     return f'{self.text[:50]}...'
    #
    # def date_in(self):
    #     return self.time_in.date()


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

    def __str__(self):
        return f'{str(self.title).upper()}'

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.pk)])

    def preview(self):
        return f'{self.text[:128]}...'
