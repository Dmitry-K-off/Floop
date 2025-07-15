"""
Custom Django management command to create forum categories.
This command allows automatically adding predefined categories to the database.
"""

from django.core.management.base import BaseCommand
from forum.models import Category


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = [
            'Танки', 'Хилы', 'ДД', 'Торговцы',
            'Гильдмастеры', 'Квестгиверы',
            'Кузнецы', 'Кожевники', 'Зельевары',
            'Мастера заклинаний'
        ]

        for category_name in categories:
            Category.objects.get_or_create(name=category_name)
