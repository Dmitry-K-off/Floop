from .models import Post, Category
# импортируем декоратор для перевода и класс настроек, от которого будем наследоваться
from modeltranslation.translator import register, TranslationOptions, translator


# регистрируем наши модели для перевода

@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('headline', 'content',) # указываем, какие именно поля надо переводить в виде кортежа

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',) # указываем, какие именно поля надо переводить в виде кортежа