import requests
import json

from Config import keys

# Класс для отсортировки ошибок ввода пользователя от ошибок программы.
class ConvertionException(Exception):
    pass

# Класс для обработки данных, введённых пользователем.
class СurrencyConverter:
    @staticmethod
    def get_price(message: str):

        """Метод принимает сообщение пользователя, извлекает из него необходимые переменные
        и проверяет их на соответствие заданному формату."""

        values = message.text.lower().split(', ') # Переменная извлекает из сообщения пользователя необходимые данные.
        if len(values) != 3: # Проверка достаточности данных.
            raise ConvertionException('неверно введены параметры.\nОбратитесь к инструкции: /help')
        quote, base, amount = values
        if not quote in keys.keys(): # Проверка верности ввода названия валюты.
            raise ConvertionException (f'не удалось обработать валюту {quote}.\nОбратитесь к списку доступных валют: /values.')
        if not base in keys.keys(): # Проверка верности ввода названия валюты.
            raise ConvertionException (f'не удалось обработать валюту {base}.\nОбратитесь к списку доступных валют: /values.')
        if keys[quote] == keys[base]: # Проверка соблюдения условия об указании разных валют.
            raise ConvertionException(f'указана одинаковая валюта {quote}.\nОбратитесь к инструкции: /help.')
        try: # Проверка верности ввода количества валюты.
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'не удалось обработать колличество валюты {amount}.\nУкажите количество числом.')
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[quote]}&tsyms={keys[base]}')
        text = f'Стоимость {amount} {quote} составляет {round(json.loads(r.content)[keys[base]] * amount, 2)} {base}.'
        return text