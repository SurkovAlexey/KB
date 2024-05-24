import telebot
import requests
from Bot_Token import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['text'])
def answer(message):
    data = {'question_raw': [message.text]}
    vopros = requests.post('https://7012.deeppavlov.ai/model', json=data).json()
    if vopros[0][0] !='':
        otvet = vopros[0][0]
        acc = round(vopros[0][1], 2)
        bot.send_message(message.chat.id, f'Ответ: {otvet}\nТочность: {acc}')
    else:
        bot.send_message(message.chat.id, 'Нет ответа на этот вопрос, напишите другой')

if __name__ == '__main__':
    bot.infinity_polling()