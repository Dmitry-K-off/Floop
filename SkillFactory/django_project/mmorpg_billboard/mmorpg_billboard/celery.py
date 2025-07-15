"""
Celery configurations.

To activate use commands:
celery -A mmorpg_billboard worker -l info --pool=solo
celery -A mmorpg_billboard beat -l INFO
"""

import os
from celery import Celery
from celery.schedules import crontab

# Set environment variable for Django settings
# This is required for Celery to locate Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mmorpg_billboard.settings')

app = Celery('mmorpg_billboard')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# Periodic task schedule (beat schedule)
app.conf.beat_schedule = {
    'notify_every_day_at_8:00': {
        'task': 'forum.tasks.send_new_announcements_notification',
        'schedule': crontab(
            hour=8,
            minute=0,
        ),
    },
}
