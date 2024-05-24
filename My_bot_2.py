import telebot
from Bot_Token import TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(
    func=lambda x: x.text.lower() in ['привет', "доброе утро", "добрый день", "добрый вечер", "здравствуйте", "ghbdtn"])
def say_hello(meassge):
    bot.send_message(meassge.chat.id, f'Здравствуй, {meassge.from_user.first_name}')


@bot.message_handler(commands=['reverse'])
def reverse(message):
    send = bot.send_message(message.chat.id, 'Какой текст необходимо перевернуть?')
    bot.register_next_step_handler(send, send_reverse_text)


def send_reverse_text(message):
    bot.send_message(message.chat.id, message.text[::-1])


if __name__ == '__main__':
    bot.infinity_polling()
