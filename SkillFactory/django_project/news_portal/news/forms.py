from django.utils.translation import gettext as _
from django import forms
from django.core.exceptions import ValidationError
from .models import Post

# Создаём формы для создания и редактирования публикаций

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, min_length=20)

    class Meta:
        model = Post
        fields = [
            'post_author',
            'post_category',
            'headline',
            'content',
        ]

        labels = {
            'post_author': _('Автор'),
            'post_category': _('Категория'),
            'headline': _('Название'),
        }

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get("content")
        headline = cleaned_data.get("headline")

        if headline == content:
            raise ValidationError({
               "headline": "Заглавие поста не должно быть идентичным его содержанию."
            })

        return cleaned_data