import telebot
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
    bot.send_message(message.chat.id, send_mess, parse_mode='html')


@bot.message_handler(commands=['game'])
def game(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    topic1 = types.KeyboardButton(db.select_category(1))
    topic2 = types.KeyboardButton(db.select_category(2))
    markup.add(topic1, topic2)
    bot.send_message(message.chat.id, 'Выбери категорию вопросов, на которую хочешь отвечать', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def text(message):
    def mess_keyboards(id_category, question_id):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        topics = [db.select_keyboards(question_id)[k] for k in range(4)]
        random.shuffle(topics)
        markup.add(*topics)
        bot.send_message(message.chat.id, db.select_question(id_category, question_id), reply_markup=markup)

    def mess_questions(id_category, first_question):
        for id_question in range(first_question, first_question + 10):
            if message.text in [db.select_keyboards(id_question)[0]]:
                db.status_question(message.chat.id, id_category, id_question, 1)
                if id_question == first_question + 9:
                    bot.send_message(message.chat.id,
                                     f'''Твой результат {db.count_result(message.chat.id, id_category)} из 10\n
Если хочешь пройти заново или выбрать другую категорию, то напиши /game''')
                else:
                    mess_keyboards(id_category, id_question + 1)
            elif message.text in [db.select_keyboards(id_question)[k] for k in range(1, 4)]:
                db.status_question(message.chat.id, id_category, id_question, 2)
                if id_question == first_question + 9:
                    bot.send_message(message.chat.id,
                                     f'''Твой результат {db.count_result(message.chat.id, id_category)} из 10\n
Если хочешь пройти заново или выбрать другую категорию, то напиши /game''')
                else:
                    mess_keyboards(id_category, id_question + 1)

    if message.text == db.select_category(1):
        bot.send_message(message.chat.id, f'''Вы выбрали категорию <b>{db.select_category(1)}</b>
Посмотрим, насколько вы Илон Маск!''', parse_mode='html')
        mess_keyboards(1, 1)
    mess_questions(1, 1)

    if message.text == db.select_category(2):
        bot.send_message(message.chat.id, f'''Вы выбрали категорию <b>{db.select_category(2)}</b>
Сейчас узнаем читали ли вы Войну и Мир!''', parse_mode='html')
        mess_keyboards(2, 11)
    mess_questions(2, 11)


bot.polling(none_stop=True)
