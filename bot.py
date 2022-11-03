import telebot
import sqlite3
from telebot import types
import config
from db import DBHelper
import random

bot = telebot.TeleBot(config.TOKEN)
db = DBHelper(config.DB_FILE)


# создание оброботчиков сообщения
@bot.message_handler(commands=['website'])
def open_website(message):
    markup = types.InlineKeyboardMarkup()  # создание кнопки внутри чата
    markup.add(types.InlineKeyboardButton('GitHub', url='https://github.com/Ilsaffff'))
    markup.add(types.InlineKeyboardButton('Telegram', url='t.me/ilsaffff'))
    bot.send_message(message.chat.id, "Хочешь связаться со мной?", parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['delete'])
def delete(message):
    db.delete_user(message.from_user.id)


@bot.message_handler(commands=['start'])
def start(message):
    db.add_user(message.from_user.id, message.from_user.username)

    send_mess = f"""
<b>Привет, {message.from_user.first_name} {message.from_user.last_name}!</b> 
Напиши /game чтобы начать играть
"""
    bot.send_message(message.from_user.id, send_mess, parse_mode='html')


@bot.message_handler(commands=['game'])
def game(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    topic1 = types.KeyboardButton(db.select_category(1))
    topic2 = types.KeyboardButton(db.select_category(2))
    markup.add(topic1, topic2)
    bot.send_message(message.chat.id, db.select_question(1, 4), reply_markup=markup)

    # bot.send_message(message.chat.id, db.select_category(1))
    # 1 - Космос 2 - Книги
    #    if user_input == DBHelper.selectCategory(1):
    #        while user_input:
    #            bot.send_message(message.chat.id, DBHelper.selectQuestion(DBHelper.selectCategory(1), range(10)),
    #                            reply_markup=markup)

    # ВОПРОС: как сделать, чтобы бот отправлял вопрос ждал ответа пользователя записывал в БД, снова задавал вопрос и
    # так далее?


bot.polling(none_stop=True)
