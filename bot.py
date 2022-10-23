import telebot
import sqlite3
from telebot import types
import set

bot = telebot.TeleBot(set.TOKEN)


# создание оброботчиков сообщения
@bot.message_handler(commands=['website'])
def open_website(message):
    markup = types.InlineKeyboardMarkup()  # создание кнопки внутри чата
    markup.add(types.InlineKeyboardButton('GitHub', url='https://github.com/Ilsaffff'))
    markup.add(types.InlineKeyboardButton('Telegram', url='t.me/ilsaffff'))
    bot.send_message(message.chat.id, "Хочешь связаться со мной?", parse_mode='html',
                     reply_markup=markup)


@bot.message_handler(commands=['start'])
def start(message):
    with sqlite3.connect('server.db') as connect:
        cursor = connect.cursor()
    # создание таблицы из файла .sql
    with open('sqlite_create_tables.sql', 'r') as sqlite_file:
        sql_script = sqlite_file.read()
    cursor.executescript(sql_script)
    connect.commit()

    # проверка на уже существущий id
    cursor.execute("SELECT * FROM users WHERE id=?", (message.from_user.id,))
    data = cursor.fetchone()
    if data is None:
        # запись данных в соотвествующие столбцы
        users = [message.chat.id, message.from_user.username]
        sqlite_insert = """INSERT INTO users 
                (id, login)
                VALUES (?,?)"""
        cursor.execute(sqlite_insert, users)
        connect.commit()

    send_mess = f"<b>Привет, {message.from_user.first_name} {message.from_user.last_name}!</b> \n" \
                "Напиши /game чтобы начать играть"
    bot.send_message(message.chat.id, send_mess, parse_mode='html')


@bot.message_handler(commands=['delete'])
def delete(message):
    # connect DB
    with sqlite3.connect('server.db') as connect:
        cursor = connect.cursor()

    # delete id from DB
    cursor.execute("DELETE from users where id=?", (message.from_user.id,))
    connect.commit()
    connect.close()


@bot.message_handler(commands=['game'])
def game(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    topic1 = types.KeyboardButton('Космос')
    topic2 = types.KeyboardButton('Книги')
    markup.add(topic1, topic2)
    bot.send_message(message.chat.id, text='Какая тема Quiz тебя интересует?', reply_markup=markup)
    # bot.send_message(message.chat.id, message)


@bot.message_handler(content_types=['text'])
def cosmos(message):
    global markup, final_message
    get_message_bot = message.text
    if get_message_bot == 'Космос':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        btn1 = types.KeyboardButton('1961')
        btn2 = types.KeyboardButton('1969')
        btn3 = types.KeyboardButton('1966')
        markup.add(btn1, btn2, btn3)
        final_message = 'В каком году человек впервые высадился на Луну?'
    elif get_message_bot == '1961' or get_message_bot == '1966':
        final_message = 'Неверно :(\n' \
                        'Посмотри, пожалуйста эту <a href="https://mediamax.am/ru/news/parzabanum/34280/">' \
                        'статью</a>\n' \
                        'И напиши снова /game'

    if get_message_bot == '1969':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        btn1 = types.KeyboardButton('7')
        btn2 = types.KeyboardButton('8')
        btn3 = types.KeyboardButton('9')
        markup.add(btn1, btn2, btn3)
        final_message = 'Сколько планет сущестувует в Солнечной системе на 2022 год?'

    elif get_message_bot == '7' or get_message_bot == '8':
        final_message = 'Неверно :(\n' \
                        'Посмотри, пожалуйста эту <a href="https://postnauka.ru/tv/64056">' \
                        'статью</a>\n' \
                        'И напиши снова /game'

    if get_message_bot == '9':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        btn1 = types.KeyboardButton('75')
        btn2 = types.KeyboardButton('65')
        btn3 = types.KeyboardButton('79')
        markup.add(btn1, btn2, btn3)
        final_message = 'Сколько спутников у Юпитера по состоянию 2018 года?'
    elif get_message_bot == '75' or get_message_bot == '65':
        final_message = 'Неверно :(\n' \
                        'Посмотри, пожалуйста эту <a href="https://starwalk.space/ru/news/jupiter-galilean-moons">' \
                        'статью</a>\n' \
                        'И напиши снова /game'
    if get_message_bot == '79':
        final_message = '<b>Молодец, ты ответил на все вопросы верно!🔥</b>\n' \
                        'А теперь можешь перейти ко второй теме, если ты ещё не решал её, написав /game\n' \
                        'Написав <b>/website</b> ты можешь связаться с создателем данного бота'

    if get_message_bot == 'Книги':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        btn1 = types.KeyboardButton('Толстой Л.Н.')
        btn2 = types.KeyboardButton('Шолохов М.А.')
        btn3 = types.KeyboardButton('Сложеницын А.И')
        markup.add(btn1, btn2, btn3)
        final_message = 'Кому принадлежит произведение "Тихий Дон"?'
    elif get_message_bot == 'Толстой Л.Н.' or get_message_bot == 'Сложеницын А.И':
        final_message = 'Неверно :(\n' \
                        'Прочитай, пожалуйста <a href="https://www.litres.ru/mihail-sholohov/tihiy-don/">' \
                        'великое произведение</a>\n' \
                        'И напиши снова /game'

    if get_message_bot == 'Шолохов М.А.':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        btn1 = types.KeyboardButton('№1')
        btn2 = types.KeyboardButton('№2')
        btn3 = types.KeyboardButton('№3')
        markup.add(btn1, btn2, btn3)
        photo1 = open('photo1.jpg', 'rb')
        bot.send_message(message.chat.id, text='№1')
        bot.send_photo(message.chat.id, photo1)
        photo2 = open('photo2.jfif', 'rb')
        bot.send_message(message.chat.id, text='№2')
        bot.send_photo(message.chat.id, photo2)
        photo3 = open('photo3.jfif', 'rb')
        bot.send_message(message.chat.id, text='№3')
        bot.send_photo(message.chat.id, photo3)
        final_message = 'На какой из картинки изображен Достовеский Ф.М.? '
    elif get_message_bot == '№2' or get_message_bot == '№3':
        final_message = 'Неверно :(\n' \
                        'Посмотри, пожалуйста<a href="https://azbyka.ru/fiction/wp-content/uploads/2017/08/864.jpg">' \
                        'портрет Достоевского</a>\n' \
                        'И напиши снова /game'
    if get_message_bot == '№1':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        btn1 = types.KeyboardButton('Москва')
        btn2 = types.KeyboardButton('Афины')
        btn3 = types.KeyboardButton('Киев')
        markup.add(btn1, btn2, btn3)
        final_message = 'В каком городе была написана летопись "Повесть временных лет"?'
    elif get_message_bot == 'Москва' or get_message_bot == 'Афины':
        final_message = 'Неверно :(\n' \
                        'Посмотри, пожалуйста' \
                        '<a href="https://azbyka.ru/otechnik/Nestor_Letopisets/povest-vremennyh-let/">' \
                        'статью о летописи</a>\n' \
                        'И напиши снова /game'
    if get_message_bot == 'Киев':
        final_message = '<b>Молодец, ты выполнил верно второй модуль!</b>\n' \
                        'Написав <b>/website</b> ты можешь связаться с создателем данного бота'
    bot.send_message(message.chat.id, text=final_message, reply_markup=markup, parse_mode='html')


bot.polling(none_stop=True)
