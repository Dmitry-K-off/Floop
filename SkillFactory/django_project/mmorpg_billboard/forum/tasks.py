"""
Project tasks
This module contains Celery tasks for handling background operations in the project.
"""
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from.models import Announcement
from datetime import datetime, timedelta

from mmorpg_billboard.settings import DEFAULT_FROM_EMAIL as host_email

"""
Celery task to send notifications about new announcements to all active users.

The task fetches all new announcements created in the last 24 hours and sends
email notifications to all active users.
"""
@shared_task
def send_new_announcements_notification():
    # Fetching all new announcements created in the last 24 hours
    new_announcements = Announcement.objects.filter(
        created_at__gte=datetime.now() - timedelta(days=1)
    )
    # If there are no new announcements, exit the function
    if not new_announcements.exists():
        return

    # Fetching all active users from the database
    users = User.objects.filter(is_active=True)

    for user in users:
        # Preparing context data for email template rendering
        context = {
            'user': user,
            'announcements': new_announcements,
        }

        # Rendering HTML and plain text versions of the email
        html_message = render_to_string('emails/new_announcements.html', context)
        plain_message = render_to_string('emails/new_announcements.txt', context)

        try:
            # Sending email to the user
            send_mail(
                'Новые объявления на форуме [MMORPG_BillBoard]',
                plain_message,
                host_email,
                [user.email],
                html_message=html_message,
                fail_silently=False
            )
        except Exception as e:
            # Logging any exceptions that occur during email sending
            print(f"Ошибка при отправке письма пользователю {user.email}: {e}")
