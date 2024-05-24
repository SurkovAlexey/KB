import telebot
from Bot_Token import TOKEN
from tic_tac_toe import *
from rpg import *
from quiz import *
from copy import deepcopy

bot = telebot.TeleBot(TOKEN) 

users = {}
ttt_dict = {}

@bot.message_handler(commands=['start'])
def send_start(message):
    txt = 'Добро пожаловать!\n'
    txt += 'Узнать что я могу /help \n'
    bot.send_message(message.chat.id, txt)

@bot.message_handler(commands=['help'])
def send_help(message):
    txt = 'Я поддерживаю следующие комманды:\n'
    txt += '/quiz - викторина\n'
    txt += '/tic_tac_toe - крестики-нолики\n'
    txt += '/game - rpg игра\n'
    bot.send_message(message.chat.id, txt)

    
@bot.message_handler(commands=['quiz'])
def start_quiz(message):
    if not message.from_user.username in users:
        # current_que - номер текущего вопроса
        # score - текущий счет
        # rank - рейтинг
        users[message.from_user.username] = {'current_que' : 1, 'score' : 0, 'rank' : None}
    else:
        users[message.from_user.username]['current_que'] = 0
        users[message.from_user.username]['score'] = 0
    que, key_quiz = choice_que()
    bot.send_message(message.chat.id, que, reply_markup=key_quiz)

@bot.callback_query_handler(func=lambda call: call.data in ['True', 'False'])
def callback_query(call):
    # Если значение True (ответ верный)
    if call.data == 'True':
        # Отправляем сообщение
        bot.send_message(call.message.chat.id, 'Верный ответ')
        # Увеличиваем счет
        users[call.from_user.username]['score'] += 1
    # Иначе, если пользователь ответил неверно
    else:
        bot.send_message(call.message.chat.id, 'Неверный ответ')
    # Увеличиваем номер вопроса
    users[call.from_user.username]['current_que'] += 1
    # Проверяем, что еще не задали 5 вопросов
    if users[call.from_user.username]['current_que'] <= 5:
        # Генерируем новый вопрос и клавиатуру
        que, key_quiz = choice_que()
        # Отправляем сообщение
        bot.send_message(call.message.chat.id, que, reply_markup=key_quiz)
    else:
        # Если это не первая игра пользователя, то у него в ключе rank есть уже какое-то значение
        if users[call.from_user.username]['rank']:
            # Пересчитываем статистику пользователя
            users[call.from_user.username]['rank'] = (users[call.from_user.username]['rank'] + (users[call.from_user.username]['score'] / 5) * 100) / 2
        else:
            # Иначе считаем статистику только за текущую игру
            users[call.from_user.username]['rank'] = (users[call.from_user.username]['score'] / 5) * 100
        # Генерируем текст для сообщения и отправляем его
        txt = f'Твой счёт - {users[call.from_user.username]["score"]}\nТвоя общая статистика - {users[call.from_user.username]["rank"]}'
        bot.send_message(call.message.chat.id, txt)

@bot.message_handler(commands=['tic_tac_toe'])
def start_tic_tac_toe(message):
    # генерация пустого поля
    ttt_dict[message.from_user.username] = ['*' for i in range(9)]
    ttk_keyboard = create_keyboard(ttt_dict[message.from_user.username])
    bot.send_message(message.chat.id, f'Ты играешь за X, ходи первым', reply_markup=ttk_keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'no' or call.data in [str(i) for i in range(9)])
def callback_query(call):
    if not call.message.text in ['Поздравляю с победой', 'На этот раз выиграл я', 'Ничья']:
        if call.data == 'no' and call.message.text != 'Эта клетка занята, выбирай другую' and '*' in ttt_dict[call.from_user.username]:
            ttk_keyboard = create_keyboard(ttt_dict[call.from_user.username])
            bot.edit_message_text('Эта клетка занята, выбирай другую', reply_markup = ttk_keyboard, chat_id=call.message.chat.id, message_id=call.message.message_id)
        elif call.data != 'no':
            ttt_dict[call.from_user.username][int(call.data)] = 'X'
            win = who_win(ttt_dict[call.from_user.username])
            if win:
                ttk_keyboard = create_keyboard(ttt_dict[call.from_user.username])
                bot.edit_message_text(win, reply_markup = ttk_keyboard, chat_id=call.message.chat.id, message_id=call.message.message_id)
            else:
                hod_b = bot_move(ttt_dict[call.from_user.username])
                ttt_dict[call.from_user.username][hod_b] = 'O'
                ttk_keyboard = create_keyboard(ttt_dict[call.from_user.username])
                win = who_win(ttt_dict[call.from_user.username])
                if win:
                    bot.edit_message_text(win, reply_markup = ttk_keyboard, chat_id=call.message.chat.id, message_id=call.message.message_id)
                else:
                    bot.edit_message_text('Делай следующий ход', reply_markup = ttk_keyboard, chat_id=call.message.chat.id, message_id=call.message.message_id)
        

@bot.message_handler(commands=['game'])
def start_game(message):
    # добавляем пользователя в словарь с значениями по умолчанию
    users_info[message.from_user.username] = {'cur_pos' : 'start', 'coins' : 0, 'items' : [], 'loc' : deepcopy(locations)}
    txt, keyboard = generate_story(message.from_user.username, users_info[message.from_user.username]['cur_pos'])
    bot.send_message(message.chat.id, txt, reply_markup=keyboard)

# если call.data в ключах словаря locations
@bot.callback_query_handler(func=lambda call: call.data in locations)
def callback_query(call):
    # меняем текущую позицию пользователя
    users_info[call.from_user.username]['cur_pos'] = call.data
    # генерируем новый текст и кнопки
    txt, keyboard = generate_story(call.from_user.username, users_info[call.from_user.username]['cur_pos'])
    # отправляем сообщение
    bot.send_message(call.message.chat.id, txt, reply_markup=keyboard)
    
# если call.data начинается с 'item '
@bot.callback_query_handler(func=lambda call: call.data.startswith('item '))
def callback_query(call):
    # берем название предмета (в строке заменяем подстроку 'item ' на '')
    item = call.data.replace('item ', '')
    # если предмет начинается на 'золото: '
    if item.startswith('золото: '):
        # то добавляем пользователю на баланс это кол-во монет
        users_info[call.from_user.username]['coins'] += int(item.replace('золото: ', ''))
    else:
        # иначе просто добавляем в список предметов
        users_info[call.from_user.username]['items'].append(item)
    # удалаляем с карты локаций этот предмет (чтобы повторно не взять)
    users_info[call.from_user.username]['loc'][users_info[call.from_user.username]['cur_pos']]['items'].remove(item)
    # сообщение о удачном деуствии
    bot.send_message(call.message.chat.id, 'Готово✔')
    # генерируем текст и кнопки и отправляем
    txt, keyboard = generate_story(call.from_user.username, users_info[call.from_user.username]['cur_pos'])
    bot.send_message(call.message.chat.id, txt, reply_markup=keyboard)

# если call.data начинается с 'exchange '
@bot.callback_query_handler(func=lambda call: call.data.startswith('exchange '))
def callback_query(call):
    # берем название предмета (в строке заменяем подстроку 'exchange ' на '')
    item1 = call.data.replace('exchange ', '')
    # берем название предмета (из словаря) , который получим
    item2 = users_info[call.from_user.username]['loc'][users_info[call.from_user.username]['cur_pos']]['exchange'][item1]
    # Если item1 начинается с 'золото: '
    
    if item1.startswith('золото: '):
        # уменьшаем кол-во монет
        # На то, что у нас достаточно монет проверять не нужно, 
        # мы это уже сделали при генереции кнопок
        users_info[call.from_user.username]['coins'] -= int(item1.replace('золото: ', ''))
    else:
        # иначе удаляем предмет
        users_info[call.from_user.username]['items'].remove(item1)
    
    # если мы меняем на золото
    if item2.startswith('золото: '):
        # увеличиваем баланс
        users_info[call.from_user.username]['coins'] += int(item2.replace('золото: ', ''))
    else:
        # иначе добавляем нам предмет
        users_info[call.from_user.username]['items'].append(item2)
    # удаляем с локации этот обмен
    users_info[call.from_user.username]['loc'][users_info[call.from_user.username]['cur_pos']]['exchange'].pop(item1)
    
    # если мы обменялись на выход, то выводим сообщение о победе
    if item2 == 'выход':
        bot.send_message(call.message.chat.id, 'Тебе удалось пройти квест')
    else:
        # иначе генерируем слудующий ход
        txt, keyboard = generate_story(call.from_user.username, users_info[call.from_user.username]['cur_pos'])
        bot.send_message(call.message.chat.id, txt, reply_markup=keyboard)

if __name__ == '__main__':
    bot.infinity_polling()