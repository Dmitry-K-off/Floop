from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Команда удаляет все посты определённой категории.'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы действительно хотите удалить все статьи в категории "{options["category"]}"? да/нет: ')

        if answer != 'да':
            self.stdout.write(self.style.ERROR('Отменено'))
            return
        try:
            category = Category.objects.get(category_name=options['category'])
            Post.objects.filter(post_category=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Посты в категории "{category.category_name}" успешно удалены.')) # в случае неправильного подтверждения говорим, что в доступе отказано
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Категории "{options['category']}" не существует.'))