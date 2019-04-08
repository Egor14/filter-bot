import telebot
from telebot.types import Message
from PIL import Image
import numpy as np
import os

TOKEN = '762705276:AAEwI7IHHTbssENWkIUqQvo3aRDejxaVU_o'

bot = telebot.TeleBot(TOKEN)


def filter(img):
    func = lambda x: 255 - x
    img = func(img)
    img = Image.fromarray(img, 'RGB')
    return img


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Пришли мне фотографию и жди результата!")


@bot.message_handler(content_types=['photo'])
def get_photo(message: Message):
    name = '{}.png'.format(message.chat.id)
    file = bot.get_file(message.photo[2].file_id)
    file = bot.download_file(file.file_path)
    with open(name, 'wb') as new_file:
        new_file.write(file)
    img = Image.open(name)
    img = np.array(img)
    img = filter(img)
    img.save(name)
    photo = open(name, 'rb')
    bot.send_photo(message.chat.id, photo)
    os.remove(name)



@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, 'Я хочу видеть только фотографии и картинки(')


bot.polling()
