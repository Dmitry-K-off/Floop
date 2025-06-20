from django.urls import path
from django.views.decorators.cache import cache_page # Импорт для кэширования.
# Импортируем созданные нами представления
from .views import PostList, PostSearch, PostDetail, NewsCreate, ArticleCreate, PostUpdate, PostDelete, \
   CategoryListView, subscribe, unsubscribe, post_limit

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем новостям у нас останется пустым.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', cache_page(10)(PostList.as_view()), name='post_list'),
   # pk — это первичный ключ объекта Post, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('article/create/', ArticleCreate.as_view(), name='article_create'),
   # Адрес страницы с сообщением о превышении лимита публикаций
   path('post/limit_reached/', post_limit, name='post_limit'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('search/', cache_page(10)(PostSearch.as_view()), name='posts_search'),

   # Путь к списку статей по выбранной категории
   path('categories/<int:pk>', cache_page(10)(CategoryListView.as_view()), name='category_list'),
   # Путь к странице с сообщением об успешной пдписке на категорию
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
   # Путь к странице с сообщением об отписке от категории
   path('categories/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe'),
]