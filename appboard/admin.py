from django.conf import settings
from django.contrib import admin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User

from .models import Post, Reply, News


class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ('get_title', 'category', 'preview', 'author', 'date_in')
    list_filter = ('author', 'category')
    search_fields = ('title', 'preview')


class ReplyAdmin(admin.ModelAdmin):
    model = Reply
    list_display = ('text', 'status', 'post', 'author', 'date_in')
    list_filter = ('status', 'author')
    search_fields = ('text', 'post')


def send_news_email(modeladmin, request, queryset): # request — инфо о запросе; queryset — объекты, выделенные галочками
    if queryset:
        queryset = queryset.order_by('pk')
        news_list = ', '.join([str(q.pk) for q in queryset])

        html_content = render_to_string(
            'board/news_send_email.html',
            {
                'news': queryset,
                'news_list': news_list,
                'link': f'{settings.SITE_URL}/board/news/',
            }
        )

        for u in User.objects.all():
            if u.email:
                msg = EmailMultiAlternatives(
                    subject=f"Новости {news_list} от Доска Объявлений",
                    body='',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[u.email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()


send_news_email.short_description = 'Рассылка новостей'


class NewsAdmin(admin.ModelAdmin):
    list_display = ('get_title', 'preview', 'author', 'date_in')
    actions = [send_news_email]


admin.site.register(Post, PostAdmin)
admin.site.register(Reply, ReplyAdmin)
admin.site.register(News, NewsAdmin)
