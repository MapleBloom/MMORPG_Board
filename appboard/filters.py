from django_filters import FilterSet, ModelChoiceFilter, DateFilter, CharFilter
from django.forms import DateInput, TextInput
from django.contrib.auth.models import User

from .models import Post, Reply, News


class PostFilter(FilterSet):
    author = ModelChoiceFilter(
        field_name='author',
        queryset=User.objects.all(),
        lookup_expr='exact',
        label=('Автор'),
        empty_label='all'
    )

    title = CharFilter(
        lookup_expr='icontains',
        label='Объявление содержит',
    )

    content = CharFilter(
        lookup_expr='icontains',
        label='В содержании объявления',
        # widget=TextInput(attrs={'class': 'form-control'}),
    )

    time_in = DateFilter(
        field_name='time_in',
        lookup_expr='gt',
        label='Опубликовано с',
        widget=DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
    )

    class Meta:
        model = Post
        fields = {
            'category': ['exact'],
        }


class ReplyFilter(FilterSet):
    author = ModelChoiceFilter(
        field_name='author',
        queryset=User.objects.all(),
        lookup_expr='exact',
        label=('Автор'),
        empty_label='all'
    )

    time_in = DateFilter(
        field_name='time_in',
        lookup_expr='gt',
        label='Получен с',
        widget=DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
    )

    class Meta:
        model = Reply
        fields = {
            'post': ['exact'],
            'status': ['exact'],
        }


class NewsFilter(FilterSet):
    time_in = DateFilter(
        field_name='time_in',
        lookup_expr='gt',
        label='Опубликовано с',
        widget=DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
    )

    title = CharFilter(
        lookup_expr='icontains',
        label='Заголовок содержит',
    )

    text = CharFilter(
        lookup_expr='icontains',
        label='Текст содержит',
        # widget=TextInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = News
        fields = ['title', 'text', 'time_in']
