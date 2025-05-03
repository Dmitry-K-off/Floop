from datetime import datetime, timedelta

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from news_portal.settings import DEFAULT_FROM_EMAIL, SITE_URL
from .models import Post, Category


@shared_task
def send_email_on_post_create(post_id): # Функция - задача для Celery, отправляющая
    # сообщение пользователям о появлении новой статьи

    # Получаем объекты класса Post
    post = Post.objects.prefetch_related('post_category').get(id=post_id)

    # Получаем уникальных подписчиков
    unique_subscribers = get_unique_subscribers(post)

    # Отправляем письма
    for email in unique_subscribers.items():
        send_email(email, post)

# Формируем кортеж уникальных пользователей
def get_unique_subscribers(post):
    unique_subscribers = {}
    for category in post.post_category.all():
        for subscriber in category.subscribers.all():
            if subscriber.email and subscriber.username not in unique_subscribers:
                unique_subscribers[subscriber.username] = subscriber.email
    return unique_subscribers

# Функция формирования и отправки сообщения
def send_email(email, post):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'link': f'{settings.SITE_URL}/posts/{post.id}',
            'text': post.preview()
        }
    )

    msg = EmailMultiAlternatives(
        subject=post.headline,
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=[email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


# Функция еженедельной рассылки уведомлений о новых постах в выбранной категории
@shared_task
def weekly_notifier():
    #  Функция отправки еженедельных сообщений
    today = datetime.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(date_time__gte=last_week)
    categories = set(posts.values_list('post_category__category_name', flat=True))
    subcribers = set(Category.objects.filter(category_name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'weekly_post.html',
        {
            'link':settings.SITE_URL,
            'posts': posts,
        }
    )
    message = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=subcribers,

    )

    message.attach_alternative(html_content, 'text/html')
    message.send()