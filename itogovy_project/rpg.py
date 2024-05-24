import telebot

users_info = {}
locations = {
    'start' : {'text' : 'Вы играете за героя, который попал в опасный лес, вам нужно найти выход в город и остаться живым', 'items' : [], 'next_move' : {'Пойти вперед' : 'forest'}, 'exchange' : {}},
    'forest' : {'text' : 'Вы попали в лес и ощутили приятный аромат сосновых деревьев, который наполнил легкие. Похоже, что вы оказались в глубине дикой природы, где еще не ощущается шум городской суеты.', 'items' : [], 'next_move' : {'Пойти налево' : 'loss',
                                                                                                                                                                                                                                           'Пойти прямо' : 'field',
                                                                                                                                                                                                                                           'Пойти направо' : 'near_the_dungeon'}, 'exchange' : {}},
    'loss' : {'text' : 'На покрытой землей каменной плите сидят темные фигуры, их глаза горят в темноте, а в руках у них ножи. Они улыбаются вам и произносят "Добро пожаловать, Наш новый друг!". Вам настолько не хватает еды и воды для того, чтобы идти дальше, что вы становитесь их жертвой и все заканчивается очень плохо.', 'items' : [], 'next_move' : {}, 'exchange' : {}},
    'field' : {'text' : 'Вы вышли в поле. Перед вам торговец.', 'items' : [], 'next_move' : {'Вернуть назад' : 'forest'}, 'exchange' : {'шкатулка' : 'золото: 3'}},
    'near_the_dungeon' : {'text' : 'Вы оказались около подземелья, которое смотрелось довольно страшно. ', 'items' : [], 'next_move' : {'Вернуться назад' : 'forest',
                                                                                                                                        'Войти внутрь' : 'dungeon',
                                                                                                                                        'Осмотреться вокруг' : 'explore'}, 'exchange' : {}},
    'explore' : {'text' : 'Осматриваясь вокруг, вы замечаете, что на стене рядом с входом кто-то нанес странные символы, которые вы не можете разгадать. Далее ты немного еще побродил с надеждой что-то найти...', 'items' : ['шкатулка'], 'next_move' : {'Вернуться к подземелью' : 'near_the_dungeon'}, 'exchange' : {}},
    'dungeon' : {'text' : 'Стены здесь полностью закрыты грубым камнем, а в воздухе царит прохлада и сырость. Похоже, что вы находитесь на начальном уровне подземелья.', 'items' : ['золото: 2'], 'next_move' : {'Пойти вперед' : 'tunnel',
                                                                                                                                                                                                                  'Выйти на улицу' : 'near_the_dungeon'}, 'exchange' : {}},
    'tunnel' : {'text' : 'Ты проходишь дальше, тут очень темно и сыро. Но вдруг в далеке ты замечаешь свет', 'items' : [], 'next_move' : {'Пойти дальше' : 'finish',
                                                                                                                                          'Вернуться' : 'dungeon'}, 'exchange' : {}},
    'finish' : {'text' : 'Концовка не за горами, но прохождение не обойдется без дополнительных расходов.', 'items' : [], 'next_move' : {'Вернуться назад' : 'tunnel'}, 'exchange' : {'золото: 5' : 'выход'}}
}

def generate_story(user, position):
    # берем текстовое описание локации
    txt = locations[position]['text']
    # создаем клавиатуру
    keyboard = telebot.types.InlineKeyboardMarkup()
    # создаем кнопки с ответами по следующим ходам
    for i in users_info[user]['loc'][position]['next_move']:
        # берем текст направления
        key_txt = i
        # берем название локации
        key_data = locations[position]['next_move'][i]
        keyboard.add(telebot.types.InlineKeyboardButton(text=key_txt, callback_data=key_data))
    # создаем кнопки для предметов, которые можно взять
    for i in users_info[user]['loc'][position]['items']:
        # берем название предмета
        key_txt = 'Взять предмет - ' + i
        # в callback_data добавим в начало 'item ', чтобы в будущем было проще разделить обработку на несколько функций
        key_data = 'item ' + i
        keyboard.add(telebot.types.InlineKeyboardButton(text=key_txt, callback_data=key_data))
    # создаем кнопки для предметов которыми можем обменяться
    for i in users_info[user]['loc'][position]['exchange']:
        # проверяем, что у нас есть нужный предмет для обмена или неообходимое кол-во монет
        if i in users_info[user]['items'] or (i.startswith('золото: ') and users_info[user]['coins'] >= int(i.replace('золото: ', ''))):
            # генерируем текст обмена
            key_txt = 'Обменять предмет ' + i + ' на ' + users_info[user]['loc'][position]['exchange'][i]
            # в callback_data добавим в начало 'exchange ', чтобы в будущем было проще разделить обработку на несколько функций
            key_data = 'exchange ' + i
            keyboard.add(telebot.types.InlineKeyboardButton(text=key_txt, callback_data=key_data))
    return (txt, keyboard)
