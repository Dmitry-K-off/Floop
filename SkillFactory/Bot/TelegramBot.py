import telebot
from Config import TOKEN, keys
from Extensions import ConvertionException, СurrencyConverter

filigree_bot = telebot.TeleBot(TOKEN)

# Функция обрабатывает команды '/start', '/help', '/values', выводит пользователю
# сообщение с инструкциями и списком валют.
@filigree_bot.message_handler(commands=['start', 'help', 'values'])
def start_help_handler(message: telebot.types.Message):
    text = ('Приветствую!\nЯ здесь, чтобы помочь Вам узнать актуальные курсы валют.\
    \nЧтобы начать работу следуйте инструкции:\n1. Введите текстовое сообщение\
    в формате <Название валюты, стоимость которой нужно узнать>, <Название валюты,\
    в которой нужно узнать стоимость>, <Количество первой валюты>;\n2. !ВАЖНО! Для получения результата\
    между названиями валют и её количеством обязательно поставьте запятые <,> и пробелы,\
    количество укажите числом;\
    \n3. Чтобы узнать список валют, доступных для подсчёта, введите команду /values;\
    \n4. Для вызова этой инструкции введите команду /help.')
    text2 = 'Инструкция:\n1. Введите текстовое сообщение\
    в формате <Название валюты, стоимость которой нужно узнать>, <Название валюты,\
    в которой нужно узнать стоимость>, <Количество первой валюты>;\n2. !ВАЖНО! Для получения результата\
    между названиями валют и её количеством обязательно поставьте запятые <,> и пробелы,\
    количество укажите числом;\
    \n3. Чтобы узнать список валют, доступных для подсчёта, введите команду /values;\
    \n4. Для вызова этой инструкции введите команду /help.'
    text3 = 'Доступные валюты:'
    if message.text == '/start':
        filigree_bot.reply_to(message, text)
    elif message.text == '/help':
        filigree_bot.reply_to(message, text2)
    elif message.text == '/values':
        for key in keys.keys():
            text3 = '\n'.join((text3, key))
        filigree_bot.send_message(message.chat.id, text3)

# Функция обрабатывает текстовые сообщения пользователя, выдаёт запрошенный результат
# или сообщает об ошибках.
@filigree_bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        text = СurrencyConverter.get_price(message)
    except ConvertionException as e:
        filigree_bot.reply_to(message, f'Ошибка пользователя:\n{e}')
    except Exception as e:
        filigree_bot.reply_to(message, f'Ошибка бота:\n{e}')
    else:
        filigree_bot.send_message(message.chat.id, text)

# Функция обрабатывает фотографии, голосовые сообщения, аудиозаписи и документы.
@filigree_bot.message_handler(content_types=['photo', 'voice', 'document', 'audio'])
def handle_docs_audio(message: telebot.types.Message):
    if message.photo:
        filigree_bot.send_message(message.chat.id, 'Красивое фото! Но я пока не могу с этим работать.')
    elif message.voice:
        filigree_bot.send_message(message.chat.id, 'У тебя приятный голос:-) Но я пока не могу с этим работать.')
    elif message.document:
        filigree_bot.send_message(message.chat.id, 'Это интересно! Но я пока не могу с этим работать.')

filigree_bot.polling(none_stop=True)