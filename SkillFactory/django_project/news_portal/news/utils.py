from django.utils import timezone
from datetime import date, timedelta

from news_portal import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Author, Post

# Функция уведомления о появлении новой статьи в категрии, на которую пописан пользователь
def send_notification(preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/posts/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

# Функция, принимающая True, если пользователь создал меньше 3-х постов в день

# Переменная, в которой содержится максимальное количество постов,
# которое доступно пользователю для создания
MAXIMUM_POST_AMOUNT = 3

# Функция, которая проверяет, чтобы пользователь не превысил
# максимальное количество публикаций
def maximum_post_amount(request):
    user = request.user
    # Получаем объект Author, связанный с пользователем
    try:
        author = Author.objects.get(authorUser=user)
    except Author.DoesNotExist:
        return 0  # Если пользователь не является автором, возвращаем 0

    # Определяем начало и конец текущего дня
    start_of_day = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)

    # Считаем количество постов за текущий день
    posts_count = Post.objects.filter(
        post_author=author,
        date_time__range=(start_of_day, end_of_day)
    ).count()

    return posts_count