from django_filters.rest_framework import filters
from django_filters import FilterSet, DateFilter, CharFilter
from .models import Post
from django import forms

# Создаем свой набор фильтров для модели Post.

class PostFilter(FilterSet):
    # Указываем поля для фильтрации

    headline = CharFilter(field_name='headline',
                          label='Заголовок содержит:',
                          lookup_expr='icontains'
                          )

    date_time = DateFilter(field_name='date_time',
                           widget=forms.DateInput(attrs={'type': 'date'}),
                           label='Посты с даты:',
                           lookup_expr='date__gte',
                           )

    class Meta:
       model = Post

# Указываем поля для фильтрации
       fields = {
           'post_author': ['exact'],
           'al_or_ns': ['exact']
       }