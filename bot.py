import telebot
from telebot import types
import config
from db import DBHelper
import random

bot = telebot.TeleBot(config.TOKEN)
db = DBHelper('context.db')


@bot.message_handler(commands=['developer'])
def open_website(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='GitHub', url='https://github.com/Ilsaffff'))
    markup.add(types.InlineKeyboardButton(text='Telegram', url='t.me/ilsaffff'))
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
    markup = types.InlineKeyboardMarkup()
    for category in db.get_categories():
        markup.add(types.InlineKeyboardButton(text=category.text, callback_data=f'cat:{category.id}'))
    bot.send_message(message.chat.id, 'Выбери категорию вопросов, на которую хочешь отвечать', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def call_back_query(call):
    global question_count, questions_max_count
    user = db.get_user(user_id=call.message.chat.id)
    if call.data.startswith('cat'):
        question_count = 0
        questions_max_count = 10
        bot.delete_message(call.message.chat.id, call.message.message_id)
        category_id = call.data.split(':')[-1]
        db.add_user_category(user_id=call.message.chat.id, category_id=category_id)
        markup = types.InlineKeyboardMarkup()
        question = db.get_next_user_question(user.id, user.category[0].id)
        for answer in question.answers:
            markup.add(types.InlineKeyboardButton(
                text=answer.text,
                callback_data=f'ans:{answer.id}'))
        bot.send_message(chat_id=call.message.chat.id, text=question.text, reply_markup=markup)
    elif call.data.startswith('ans'):
        question_count = question_count + 1
        bot.delete_message(call.message.chat.id, call.message.message_id)
        answer_id = call.data.split(':')[-1]
        db.add_user_answer(call.message.chat.id, answer_id)
        question = db.get_next_user_question(user.id, user.category[0].id)
        if question_count < questions_max_count:
            markup = types.InlineKeyboardMarkup()
            for answer in question.answers:
                markup.add(types.InlineKeyboardButton(text=answer.text, callback_data=f'ans:{answer.id}'))
            bot.send_message(chat_id=call.message.chat.id, text=question.text, reply_markup=markup)
        else:
            result = db.get_result(user_id=call.message.chat.id, questions_max_count=questions_max_count)
            markup = types.InlineKeyboardMarkup()
            for category in db.get_categories():
                markup.add(types.InlineKeyboardButton(text=category.text, callback_data=f'cat:{category.id}'))
            bot.send_message(call.message.chat.id,
                             f'Твой результат: {result}\nЕсли хочешь ещё поотвечать, то выбери категориюю вопросов',
                             reply_markup=markup)


bot.polling(none_stop=True)
