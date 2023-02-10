from django_filters import FilterSet, ModelChoiceFilter, ModelMultipleChoiceFilter, DateFilter, CharFilter
from django.forms import DateInput, TextInput

from .models import News


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


# class CategoryFilter(FilterSet):
#     category = ModelChoiceFilter(
#         field_name='category',
#         queryset=Category.objects.all(),
#         label='',
#     )
#
#     author = ModelChoiceFilter(
#         field_name='author',
#         queryset=Author.objects.all(),
#         lookup_expr='exact',
#         label=gettext_lazy('Author'),
#         empty_label='all'
#     )
