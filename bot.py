import telebot
from telebot import types
import config
from db import DBHelper
import random


class User:
    question_id = 0
    questions_id = []
    number_question = 1
    category_id = 0


bot = telebot.TeleBot(config.TOKEN)
db = DBHelper(config.DB_FILE)
user = User()


@bot.message_handler(commands=['developer'])
def open_website(message):
    markup = types.InlineKeyboardMarkup()  # создание кнопки внутри чата
    markup.add(types.InlineKeyboardButton('GitHub', url='https://github.com/Ilsaffff'))
    markup.add(types.InlineKeyboardButton('Telegram', url='t.me/ilsaffff'))
    bot.send_message(message.chat.id, "Хочешь связаться со разработчиком?", parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['delete'])
def delete(message):
    db.delete_user(message.from_user.id)


@bot.message_handler(commands=['start'])
def start(message):
    db.add_user(message.from_user.id, message.from_user.username)
    send_mess = f"""
<b>Привет, {message.from_user.first_name}!</b> 
Напиши /game чтобы начать играть
"""
    bot.send_message(message.chat.id, send_mess, parse_mode='html')


@bot.message_handler(commands=['game'])
def game(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*db.get_categories())
    bot.send_message(message.chat.id, 'Выбери категорию вопросов, на которую хочешь отвечать', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def text(message):
    def send_question(question_id):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        topics = db.select_buttons(question_id)
        random.shuffle(topics)
        markup.add(*topics)
        bot.send_message(message.chat.id, db.get_question(question_id), reply_markup=markup)

    if message.text in db.get_categories():
        user.number_question = 0
        user.category_id = db.get_id_category(message.text)
        user.questions_id = db.get_id_questions(user.category_id)
        random.shuffle(user.questions_id)
        user.question_id = user.questions_id[user.number_question]
        send_question(user.question_id)

    if message.text in db.select_buttons(user.question_id):
        db.status_question(message.chat.id, message.text)
        if user.number_question != len(user.questions_id) - 1:
            user.number_question += 1
            user.question_id = user.questions_id[user.number_question]
            send_question(user.question_id)
        else:
            user.number_question = 0
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            markup.add(*db.get_categories())
            bot.send_message(message.chat.id, f'Ты ответил верно по категории <b>{db.select_category(user.category_id)}'
                                              f'</b> на <b>{db.count_result(message.from_user.id, user.category_id)}'
                                              f' вопросов из {len(user.questions_id)} </b>\n'
                                              'Далее можешь пройти ещё раз по любой другой категории! \n'
                                              '<b>Если хочешь связаться с разработчиком бота, то напиши /developer</b>',
                             parse_mode='html', reply_markup=markup)


bot.polling(none_stop=True)
