from django.contrib import admin
from .models import Author, Category, Comment, Post

# Register your models here.


class AuthorAdmin(admin.ModelAdmin):  # доабляем в админ-панель отображение и фильтрацию объектов таблицы Author
    list_display = ['get_name','authorUser__username', 'rating']  # добавляем отображение полей в админ-панель
    list_filter = ('authorUser__username', 'rating')  # добавляем фильтры в админ-панель
    search_fields = ('authorUser__username', )  # тут всё очень похоже на фильтры из запросов в базу


class CategoryAdmin(admin.ModelAdmin):  # доабляем в админ-панель отображение и фильтрацию объектов таблицы Category
    list_display = ['category_name']  # добавляем отображение полей в админ-панель
    list_filter = ['category_name']  # добавляем фильтры в админ-панель


class CommentAdmin(admin.ModelAdmin):  # доабляем в админ-панель отображение и фильтрацию объектов таблицы Comment
    list_display = ['get_name','user_comm', 'text_comm', 'rating']  # добавляем отображение полей в админ-панель
    list_filter = ['user_comm', 'text_comm', 'rating']  # добавляем фильтры в админ-панель


class PostAdmin(admin.ModelAdmin):  # доабляем в админ-панель отображение и фильтрацию объектов таблицы Comment
    list_display = ['get_author', 'post_author', 'formated_date_time', 'headline', 'rating']  # добавляем отображение полей в админ-панель
    list_filter = ['post_author', 'rating']  # добавляем фильтры в админ-панель


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)