import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_shop.settings')

app = Celery('project_shop')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# Команда для запуска: celery -A project_shop worker --pool=solo -l INFO