import random
import telebot
from Bot_Token import TOKEN
bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['rand'])
def rand(message):
    bot.send_message(message.chat.id,f'Случайное число: {random.randint(1,100)}')

@bot.message_handler(content_types=['text'])
def echo(message):
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    bot.infinity_polling()