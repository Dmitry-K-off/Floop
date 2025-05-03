from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils import formats
from django.urls import reverse

# Create your models here.

class Author (models.Model):
# Модель, содержащая объекты всех авторов.
# Имеет следующие поля:
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE) # cвязь «один к одному» с
# встроенной моделью пользователей User.
    rating = models.IntegerField(default=0) # рейтинг пользователя.

    def update_rating(self): # Метод, который обновляет рейтинг текущего автора:
        auth_posts_rating = self.post_set.aggregate(apr=Coalesce(Sum('rating'), 0))['apr'] # суммарный рейтинг каждой статьи автора умножается на 3;
        auth_comments_rating = self.authorUser.comment_set.aggregate(acr=Coalesce(Sum('rating'), 0))['acr'] # суммарный рейтинг всех комментариев автора;
        users_underpostcomments_rating = self.post_set.aggregate(uur=Coalesce(Sum('comment__rating'), 0))['uur'] # суммарный рейтинг всех комментариев к статьям автора.
        self.rating = auth_posts_rating*3 + auth_comments_rating + users_underpostcomments_rating
        self.save()

    def __str__(self):
        return self.authorUser.username


class Category (models.Model):
# Модель "Категории" новостей/статей.
    category_name = models.CharField(max_length=255, unique=True) # Модель имеет поле:
# название категории. По заданию поле должно быть уникальным.

    # Поле subscribers создано для реализации возможности подписки пользователей на конкретные категрии.
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='categories')

    def __str__(self):
      return self.category_name


class Post (models.Model):
# По заданию Модель должна содержать в себе статьи и новости, которые создают пользователи.
# Каждый объект может иметь одну или несколько категорий.
# Соответственно, модель должна включать следующие поля:
    article = 'AL' # Переменная, устанавливающая ограничение выбора в поле "al_or_ns".
    news = 'NS' # Переменная, устанавливающая ограничение выбора в поле "al_or_ns".
    OPTIONS = [
        (article, "Cтатья"),
        (news, "Новость")
    ] # Переменная, устанавливающая ограничение выбора в поле "al_or_ns".
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE) # связь «один ко многим» с моделью Author;
    al_or_ns = models.CharField(max_length=2, choices=OPTIONS, default='AL') # поле с выбором — «статья» или «новость»;
    date_time = models.DateTimeField(auto_now_add=True) # автоматически добавляемая дата и время создания;
    post_category = models.ManyToManyField(Category, through='PostCategory') # связь «многие ко многим»
# с моделью Category (с дополнительной моделью PostCategory);
    headline = models.CharField(max_length=255) # заголовок статьи/новости;
    content = models.TextField() # текст статьи/новости;
    rating = models.IntegerField(default=0) # рейтинг статьи/новости;

    def like(self): # Метод, который увеличивает рейтинг публикации на единицу.
        self.rating += 1
        self.save()

    def dislike (self): # Метод, который уменьшает рейтинг публикации на единицу.
        self.rating -= 1
        self.save()

    def preview(self): # Метод, который возвращает начало статьи (предварительный просмотр)
        # длиной 124 символа и добавляет многоточие в конце.
        return self.content[0:123] + '...'

    def formated_date_time(self):
        return formats.date_format(self.date_time, "d.m.Y | H:m")

    def type_post(self):
        return dict(self.OPTIONS)[self.al_or_ns]


    def __str__(self):
        return f'{self.date_time.strftime("%d.%m.%Y")}, {dict(self.OPTIONS)[self.al_or_ns]}: {self.headline.title()}, Автор - {self.post_author.authorUser.username}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

class PostCategory (models.Model):
# Промежуточная модель для связи «многие ко многим»:
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # связь «один ко многим» с моделью Post;
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # связь «один ко многим» с моделью Category.


class Comment (models.Model):
# Под каждой новостью / статьёй можно оставлять комментарии, поэтому необходимо организовать
# их способ хранения тоже. Модель будет иметь следующие поля:
    post_comm = models.ForeignKey(Post, on_delete=models.CASCADE) # связь «один ко многим» с моделью Post;
    user_comm = models.ForeignKey(User, on_delete=models.CASCADE) # связь «один ко многим» со
# встроенной моделью User (комментарии может оставить любой пользователь, необязательно автор);
    text_comm = models.TextField(max_length=2500) # текст комментария;
    datetime_comm = models.DateTimeField(auto_now_add=True) # дата и время создания комментария;
    rating = models.IntegerField(default=0) # рейтинг комментария.

    def like(self): # Метод, который увеличивает рейтинг комментария на единицу.
        self.rating += 1
        self.save()

    def dislike(self): # Метод, который уменьшает рейтинг комментария на единицу.
        self.rating -= 1
        self.save()

    def __str__(self):
      return f'{self.text_comm[:50]}... Автор: {self.user_comm}'