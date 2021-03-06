import logging
import os

import requests

from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Updater

from dotenv import load_dotenv

load_dotenv()

secret_token = os.getenv('TOKEN')
# Взяли переменную TOKEN из пространства переменных окружения

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO, filename='bot_log.log', filemode='w')

URL = 'https://api.thecatapi.com/v1/images/search'

def get_new_image():
    try:
        response = requests.get(URL)
    except Exception as error:
        # print(error)
        logging.error(f'Ошибка при запросе к основному API: {error}')      
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url)
    response = response.json()
    random_cat = response[0].get('url')
    return random_cat

def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())

def say_hi(update, context):
    # Получаем информацию о чате, из которого пришло сообщение,
    # и сохраняем в переменную chat
    chat = update.effective_chat
    # В ответ на любое текстовое сообщение 
    # будет отправлено 'Привет, я KittyBot!'
    context.bot.send_message(chat_id=chat.id, text='Привет! Я КотБот и скоро я научусь отправлять тебе красивые фотографии котиков. Мой создатель Игорь Лисянский @lsnsky')

def wake_up(update, context):
    # В ответ на команду /start 
    # будет отправлено сообщение 'Спасибо, что включили меня'
    chat = update.effective_chat
    name = update.message.chat.first_name
    # Вот она, наша кнопка.
    # Обратите внимание: в класс передаётся список, вложенный в список, 
    # даже если кнопка всего одна.
    button = ReplyKeyboardMarkup([['/newcat']], resize_keyboard=True)
    # print(update)
    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}. Посмотри, какого котика я тебе нашёл'.format(name),
        reply_markup=button
    )
    context.bot.send_photo(chat.id, get_new_image())

# Регистрируется обработчик CommandHandler;
# он будет отфильтровывать только сообщения с содержимым '/start'
# и передавать их в функцию wake_up()
def main():
    updater = Updater(token=secret_token)
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('newcat', new_cat))
    
    updater.start_polling()
    updater.idle() 

if __name__ == '__main__':
    main()

