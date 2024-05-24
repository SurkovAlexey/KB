import telebot
from Bot_Token import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['video'])
def send_text(message):
    file = bot.get_file(message.video.file_id)
    load_file = bot.download_file(file.file_path)
    bot.send_video_note(message.chat.id, load_file)

if __name__ == '__main__':
    bot.infinity_polling()
