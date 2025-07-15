from django import forms

from .models import Announcement, Response

# Form class for creating and editing Announcement objects
class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['category', 'title', 'content', 'images', 'videos']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select category-select'}),
            'title': forms.TextInput(attrs=
                {'class': 'form-control title-input',
                 'placeholder': 'Введите заголовок'}),
            'content': forms.Textarea(attrs={
                'class': 'form-control content-textarea',
                'rows': 5,
                'placeholder': 'Введите текст объявления'
            }),
            'images': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
            'videos': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'video/*',
            })
        }

# Form class for creating Response objects
class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Введите текст, чтобы откликнуться на объявление'
                }
            ),
        }
