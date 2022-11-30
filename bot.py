import telebot
from telebot import types
import config
from db import DBHelper
import random

bot = telebot.TeleBot(config.TOKEN)
db = DBHelper('test.db')


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
        markup.add(types.InlineKeyboardButton(text=str(category), callback_data=f'category:{category.id}'))
    bot.send_message(message.chat.id, 'Выбери категорию вопросов, на которую хочешь отвечать', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def call_back_query(call):
    global questions, question_count, questions_max_count
    if call.data.startwith('category'):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        category_id = int(''.join(filter(str.isdigit, call.data)))
        questions = db.get_categories()[category_id - 1].questions
        question_count = 0
        questions_max_count = 10
        markup = types.InlineKeyboardMarkup()
        question = random.choice(questions)
        for answer in question.answers:
            markup.add(types.InlineKeyboardButton(text=str(answer), callback_data=f'answer:{answer.id}'))
        bot.send_message(call.message.chat.id, question, reply_markup=markup)
    elif call.data.startwith('answer'):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        answer_id = int(''.join(filter(str.isdigit, call.data)))
        db.add_user_answer(call.message.chat.id, answer_id)
        question_count = question_count + 1
        question = random.choice(questions)
        if question_count < questions_max_count:
            markup = types.InlineKeyboardMarkup()
            for answer in question.answers:
                markup.add(types.InlineKeyboardButton(text=str(answer), callback_data=f'answer:{answer.id}'))
            bot.send_message(call.message.chat.id, question, reply_markup=markup)
        else:
            result = db.get_result(user_id=call.message.chat.id, questions_max_count=questions_max_count)
            bot.send_message(call.message.chat.id, f'Твой результат: {result}', reply_markup=None)


bot.polling(none_stop=True)
