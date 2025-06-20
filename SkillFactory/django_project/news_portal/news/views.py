from lib2to3.fixes.fix_input import context

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.urls import reverse_lazy, reverse
from django.views import View
from django.http.response import HttpResponse
from django.utils.translation import activate, get_supported_language_variant, get_language_from_request
from django.utils import timezone
import pytz
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Author, Post, Category
from .filters import PostFilter
from .forms import PostForm
from .tasks import send_email_on_post_create
from .utils import maximum_post_amount, MAXIMUM_POST_AMOUNT


# Create your views here.


class Index(View):
    def get(self, request):
        current_time = timezone.now()
        models = Post.objects.all()

        context = {
            'models': models,
            'current_time': current_time,
            'timezones': pytz.common_timezones,
            'selected_timezone': request.session.get('django_timezone'),
        }

        return render(request, 'protect/index.html', context)

    def post(self, request):
        timezone_str = request.POST.get('timezone')

        if timezone_str and timezone_str in pytz.common_timezones:
            request.session['django_timezone'] = timezone_str
        else:
            request.session['django_timezone'] = timezone.get_default_timezone_name()

        return redirect('/')


class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-date_time'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 10  # Указаем количество записей на странице

    # # testtesttest
    # def get(self, request):
    #     current_time = timezone.now()
    #
    #     # .  Translators: This message appears on the home page only
    #     models = Post.objects.all()
    #     context = {
    #         'models': models,
    #         'current_time': timezone.now(),
    #         'timezones': pytz.common_timezones  # добавляем в контекст все доступные часовые пояса
    #     }
    #
    #     return HttpResponse(render(request, 'posts.html', context))
    #
    # #  по пост-запросу будем добавлять в сессию часовой пояс, который и будет обрабатываться написанным нами ранее middleware
    # def post(self, request):
    #     request.session['django_timezone'] = request.POST['timezone']
    #     return redirect('/posts')
    # # testtesttest


class PostSearch(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-date_time'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'search.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 10  # Указаем количество записей на странице

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список постов
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному посту
    model = Post
    # Используем другой шаблон — post.html
    template_name = 'post.html'
    queryset = Post.objects.all()
    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj
    # Название объекта, в котором будет выбранный пользователем пост
    context_object_name = 'post'


# Добавляем представление для создания новостей.
# Добавляем проверку на наличие права на создание новости.
class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    # Указываем форму
    form_class = PostForm
    # модель пост
    model = Post

    # Шаблон, в котором используется форма.
    template_name = 'news_create.html'

    # Представление предупреждает о превышении количества постов
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not maximum_post_amount(request) < MAXIMUM_POST_AMOUNT:
            return redirect(reverse('post_limit'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.al_or_ns = 'NS'
        post.save()
        send_email_on_post_create.delay(post_id=post.id) # Постановка задачи для Celery.
        return super().form_valid(form)


# Добавляем представление для создания статей.
# Добавляем проверку на наличие права на создание статьи.
class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    # Указываем форму
    form_class = PostForm
    # модель пост
    model = Post

    # Шаблон, в котором используется форма.
    template_name = 'article_create.html'

    # Представление предупреждает о превышении количества постов
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not maximum_post_amount(request) < MAXIMUM_POST_AMOUNT:
            return redirect(reverse('post_limit'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.al_or_ns = 'AL'
        post.save()
        send_email_on_post_create.delay(post_id=post.id) # Постановка задачи для Celery.
        return super().form_valid(form)


# Добавляем представление для изменения поста.
# Добавляем проверку на наличие права на редактирование.
class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    form_class = PostForm
    model = Post
    template_name = 'post_update.html'

# Представление, удаляющее пост.
# Добавляем проверку на наличие права на удаление поста.
class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

# Представление, позволяющее сформировать список публикаций, в выбранной категории
class CategoryListView(PostList):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(post_category=self.category)
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

# Представление, позволяющее подписаться на категорию
@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = 'Вы успешно подписались на рассылку новостей в категории'
    return render(request, 'subscribe.html', {'category': category, 'message': message})

# Представление, позволяющее отписаться от категории
@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)
    message = 'Вы отписались от рассылки новостей в категории'
    return render(request, 'unsubscribe.html', {'category': category, 'message': message})

def post_limit(request):
    return render(request, 'post_limit.html')