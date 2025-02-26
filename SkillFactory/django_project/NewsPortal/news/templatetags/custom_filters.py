from django import template

"""

Добавялем фильтр "censor",
который заменяет буквы нежелательных слов в заголовках
и текстах статей на символ «*».

"""

register = template.Library()

# Список запрещённых слов.
bad_words = ['редиска',
             'Редиска',
             'хрен',
             'Хрен',
             'хирабора',
             'Хирабора'
             ]

def giveme_stars(word): #Функция добавляет символ "звёздочка" (*) в запрещённые слова
    corrected_word = word[0]
    for lr in word[1:]:
        lr = '*'
        corrected_word += lr
    return corrected_word

@register.filter()
def censor(statement): # функция отфильтровывает запрещённые слова, добавляя звёздочки такие слова после первой буквы.
    corrected_statement = statement
    for bad_word in bad_words:
        corrected_statement = corrected_statement.replace(bad_word,
                                                          giveme_stars(bad_word))
    return corrected_statement