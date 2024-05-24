import random
import telebot

questions = {
    'Сколько будет 2 + 2?' : {'4' : True, '5' : False, '6' : False},
    'Какая столица России' : {'Санкт-Петербург' : False, 'Москва' : True},
    'Создатель ЯП Python' : {'Гвидо ван Россум' : True, 'Джон Маккарти' : False},
    'Известный код из Матрицы на самом деле обозначает …' : {'Рецепт суши' : True, 'Случайный набор символов' : False},
    'Самая большая планета' : {'Юпитер' : True, 'Сатурн' : False}
}

def choice_que():
    # выбираем случайный вопрос
    que = random.choice(list(questions.keys()))
    # достаем для него словарь ответов
    ans = questions[que]
    # создаем клавиатуру
    key_quiz = telebot.types.InlineKeyboardMarkup()
    # создаем кнопки с ответами
    for i in ans:
        key_quiz.add(telebot.types.InlineKeyboardButton(text=i, callback_data=str(ans[i])))
    return (que, key_quiz)