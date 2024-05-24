import telebot
import requests
from Bot_Token import TOKEN

bot = telebot.TeleBot(TOKEN)

def get_adress(lat, lon):
    url = f'https://geocode.maps.co/reverse?lat={lat}&lon={lon}'
    r = requests.get(url).json()['display_name']
    return r

@bot.message_handler(commands=['start'])
def weather (message):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = telebot.types.KeyboardButton(text='Поделиться местоположением', request_location = True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, 'Поделись местоположением', reply_markup=keyboard)

@bot.message_handler(content_types=['location'])
def location(message):
    a = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, get_adress(message.location.latitude, message.location.longitude), reply_markup=a)

if __name__ == '__main__':    
    bot.infinity_polling()
