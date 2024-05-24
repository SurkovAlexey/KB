import random
import telebot

def create_keyboard(map):
    # список для строк кнопок (в каждой строке 3 кнопки)
    ttk_buttons = []
    # цикл по строкам
    for i in range(3):
        # список строки
        row = []
        # цикл по кнопкам в строке
        for j in range(3):
            # если в поле пусто
            if map[i * 3 + j] == '*':
                row.append(telebot.types.InlineKeyboardButton(text='⬜', callback_data=str(i * 3 + j)))
            # если стоит крестик
            elif map[i * 3 + j] == 'X':
                row.append(telebot.types.InlineKeyboardButton(text='✖', callback_data='no'))
            # если стоит нолик
            elif map[i * 3 + j] == 'O':
                row.append(telebot.types.InlineKeyboardButton(text='⭕', callback_data='no'))
        # добавляем строку
        ttk_buttons.append(row)
    # создаем клавиатуру
    ttt_key_map = telebot.types.InlineKeyboardMarkup(ttk_buttons, row_width=3)
    return ttt_key_map

# генерация хода бота
def bot_move(map):
    # выбираем случайную клетку
    ans = random.randint(0, 8)
    # пока сгенерированная клетка не пустая
    while map[ans] != '*':
        # генерируем клетку
        ans = random.randint(0, 8)
    return ans

def who_win(map):
    if map[0] == map[1] == map[2] == 'X' or \
        map[3] == map[4] == map[5] == 'X' or \
        map[6] == map[7] == map[8] == 'X' or \
        map[0] == map[3] == map[6] == 'X' or \
        map[1] == map[4] == map[7] == 'X'or  \
        map[2] == map[5] == map[8] == 'X' or \
        map[0] == map[4] == map[8] == 'X' or \
        map[2] == map[4] == map[6] == 'X': 
       return 'Поздравляю с победой'
    elif map[0] == map[1] == map[2] == 'O' or \
        map[3] == map[4] == map[5] == 'O' or \
        map[6] == map[7] == map[8] == 'O' or \
        map[0] == map[3] == map[6] == 'O' or \
        map[1] == map[4] == map[7] == 'O'or  \
        map[2] == map[5] == map[8] == 'O' or \
        map[0] == map[4] == map[8] == 'O' or \
        map[2] == map[4] == map[6] == 'O': 
        return 'На этот раз выиграл я'
    elif not '*' in map:
        return 'Ничья'