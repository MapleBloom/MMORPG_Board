from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category',
                  'title',
                  'content',
                  ]
        labels = {
            'content': 'Содержание - форматируйте текст, сохраняйте изображения и ссылки на Youtube',
        }

    def clean(self):
        cleaned_data = super().clean()
        title, content = cleaned_data.get('title', ''), cleaned_data.get('content', '')
        if title is not None and title.lower() in content.lower():
            err_text = 'Избегайте повтора текста объявления в содержании.'
            raise ValidationError({'title': err_text})
        return cleaned_data

    def clean_title(self):
        title = self.cleaned_data['title']
        if title and title[0].islower():
            raise ValidationError('Начните объявление с заглавной буквы.')
        return title
