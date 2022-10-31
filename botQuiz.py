import telebot
import sqlite3
from telebot import types
import set
from DataBaseHelper import DBHelper
import random

bot = telebot.TeleBot(set.TOKEN)


# создание оброботчиков сообщения
@bot.message_handler(commands=['website'])
def open_website(message):
    markup = types.InlineKeyboardMarkup()  # создание кнопки внутри чата
    markup.add(types.InlineKeyboardButton('GitHub', url='https://github.com/Ilsaffff'))
    markup.add(types.InlineKeyboardButton('Telegram', url='t.me/ilsaffff'))
    bot.send_message(message.chat.id, "Хочешь связаться со мной?", parse_mode='html',
                     reply_markup=markup)


@bot.message_handler(commands=['delete'])
def delete(message):
    DBHelper.deleteUser(message.from_user.id)


@bot.message_handler(commands=['start'])
def start(message):
    DBHelper.addUserinTable(message.from_user.id, message.from_user.username)
    send_mess = f"""
<b>Привет, {message.from_user.first_name} {message.from_user.last_name}!</b> 
Напиши /game чтобы начать играть
"""
    bot.send_message(message.from_user.id, send_mess, parse_mode='html')


@bot.message_handler(commands=['game'])
def game(message):
    user_input = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    topic1 = types.KeyboardButton(DBHelper.selectCategory(1))
    topic2 = types.KeyboardButton(DBHelper.selectCategory(2))
    markup.add(topic1, topic2)
    # 1 - Космос 2 - Книги
    #    if user_input == DBHelper.selectCategory(1):
    #        while user_input:
    #            bot.send_message(message.chat.id, DBHelper.selectQuestion(DBHelper.selectCategory(1), range(10)),
    #                            reply_markup=markup)

    # ВОПРОС: как сделать, чтобы бот отправлял вопрос ждал ответа пользователя записывал в БД, снова задавал вопрос и
    # так далее?

    bot.send_message(message.chat.id, DBHelper.selectQuestion(DBHelper.selectCategory(1), 5), reply_markup=markup)


bot.polling(none_stop=True)
