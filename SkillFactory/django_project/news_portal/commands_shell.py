# ВЫЗОВ КОНСОЛИ shell
# ...\news_portal> python manage.py shell

# В консоли shell:

# ИМПОРТИРУЕМ ДАННЫЕ:
# from news.models import *

# 1. Создаём двух пользователей (с помощью метода User.objects.create_user('username'))

# user1 = User.objects.create_user(username='Андрей', password='12345')
# user2 = User.objects.create_user(username='Игнат', password='12345')
# user3 = User.objects.create_user(username='Алевтина', password='12345')
# user4 = User.objects.create_user(username='Мария', password='12345')

# 2. Создаём два объекта модели Author, связанные с пользователями:

# author1 = Author.objects.create(authorUser=user1)
# author2 = Author.objects.create(authorUser=user2)

# 3. Добавляем 4 категории в модель Category:

# category1 = Category.objects.create(category_name='Последние новости')
# category2 = Category.objects.create(category_name='Новости региона')
# category3 = Category.objects.create(category_name='Новости спорта')
# category4 = Category.objects.create(category_name='Новости технологий')

# 4. Добавить 2 статьи и 1 новость:

# article1 = Post.objects.create(
#     post_author = author1,
#     headline = 'Мы ещё вернёмся!',
#     content = 'Вице-президент Федерации хоккея России Роман Ротенберг объявил о возможном'
#               'возвращении молодёжной сборной России на чемпионат мира 2026 года.'
#               'Это стало возможным благодаря давлению со стороны канадской телекомпании TSN,'
#               'которая выразила недовольство отсутствием российской команды.'
#               'Ожидается, что подробности будут объявлены на предстоящем Турнире четырёх наций,'
#               'который пройдёт с 12 по 18 февраля в Монреале и Бостоне.'
# )

# article2 = Post.objects.create(
#     post_author = author2,
#     headline = 'Будущее у Вас в кармане',
#     content = 'На вчерашней выставке достижений современных технологий был представлен новый смартфон'
#               'CHPOCO X500, который оснащён новейшим голографическим дисплеем, камерой на 100000 мегапикселей'
#               '"HublePRO" и аккумулятором на термоядерном синтезе. Будущее уже здесь!'
# )

# news1 = Post.objects.create(
#     post_author = author2,
#     al_or_ns = 'NS',
#     headline = 'Новый рейс самолета',
#     content ='УРА! Компания FastPlane запустила рейс из нашего чудесного горда в Пекин. '
#               'Стоимость билета 90000 рублей по скидке.Успейте заказать!!'
# )

# 5. Присваиваем статьям/новостям категории (как минимум в одной статье/новости должно быть не меньше 2 категорий):

# article1.post_category.add(category3)
# article2.post_category.add(category4)
# news1.post_category.add(category2)
# article1.post_category.add(category1)
# article2.post_category.add(category1)

# 6. Создаём как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий):
#
# comment1 = Comment.objects.create(
#     post_comm = article1,
#     user_comm = user2,
#     text_comm = 'Я очень давно этого жду!'
# )

# comment2 = Comment.objects.create(
#     post_comm = article2,
#     user_comm = user1,
#     text_comm = 'Ура!! Наконец-то, можно заряжать телефон не каждый день!'
# )

# comment3 = Comment.objects.create(
#     post_comm = news1,
#     user_comm = user4,
#     text_comm = 'А там сейчас как раз Новый Год празднуют!'
# )

# comment4 = Comment.objects.create(
#     post_comm = article2,
#     user_comm = user3,
#     text_comm = 'А сколько это "чудо" техники будет стоить?'
# )

# comment5 = Comment.objects.create(
#     post_comm = article1,
#     user_comm = user1,
#     text_comm = 'А я поеду на этот турнир!'
# )

# comment6 = Comment.objects.create(
#     post_comm = article1,
#     user_comm = user4,
#     text_comm = 'Эта статья больше похожа на шутку нейросети:( Дизлайк!'
# )

# 7. Применяем функции like() и dislike() к статьям/новостям и комментариям, чтобы
# скорректировать рейтинги этих объектов:

# for i in range(11):
#     article2.like()

# article2.dislike()

# for i in range(15):
#    article1.dislike()

# for i in range(10):
#     news1.like()

# for i in range(16):
#     comment2.like()

# for i in range(5):
#     comment5.dislike()

# 8. Обновляем рейтинги пользователей

# author1.update_rating()
# author2.update_rating()

# 9. Выводим username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля
# первого объекта):

# best_author = Author.objects.order_by('-rating')[:1][0] # создаём переменную для комфортного
# написания дальнейших команд, отсортировав и "отрезав" автора с наибольшим рейтингом.

# print(f'Имя лучшего пользователя - {best_author.authorUser.username}! '
#       f'Его рейтинг - {best_author.rating}!!')

# 10. Выводим дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи,
# основываясь на лайках/дислайках к этой статье:

# best_article = Post.objects.order_by('-rating').filter(al_or_ns='AL')[:1][0]  # отфильтровываем
# посты типа "Статья (AL)", сортируем их по рейтингу и "отрезаем" тот, у которого рейтинг наивысший.

# print(f'Дата добавления поста: {best_article.date_time.strftime('%d.%m.%Y')}, '
#       f'Автор - {best_article.post_author.authorUser.username}, '
#       f'Рейтинг поста {best_article.rating}, '
#       f'Заголовок: {best_article.headline}, '
#       f'Превью: {best_article.preview()} '
#       )

# 11. Выводим все комментарии (дата, пользователь, рейтинг, текст) к этой статье:

# Используем цикл for

# for under_pst_comm in Comment.objects.filter(post_comm=best_article):
#     print(f'Дата добавления комментария: {under_pst_comm.datetime_comm.strftime('%d.%m.%Y')}, '
#         f'Автор поста - {under_pst_comm.user_comm.username}, '
#         f'Рейтинг поста {under_pst_comm.rating}, '
#         f'Текст: {under_pst_comm.text_comm}, '
#     )