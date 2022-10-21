import telebot  # Импорт библиотеки по созданию телеграмм бота
from telebot import types

bot = telebot.TeleBot('5472326831:AAGllSHgFRGcvyXj-sPsEPmZSTGDwnHFwt0')


@bot.message_handler(commands=['website'])
def open_website(message):
    markup = types.InlineKeyboardMarkup()  # создание кнопки
    markup.add(types.InlineKeyboardButton('GitHub', url='https://github.com/Ilsaffff'))
    markup.add(types.InlineKeyboardButton('Telegram', url='t.me/ilsaffff'))
    bot.send_message(message.chat.id, "Хочешь связаться со мной?", parse_mode='html',
                     reply_markup=markup)


@bot.message_handler(commands=['start'])
def start(message):
    send_mess = f"<b>Привет, {message.from_user.first_name} {message.from_user.last_name}!</b> \n" \
                f"Напиши /game чтобы начать играть"
    bot.send_message(message.chat.id, send_mess, parse_mode='html')


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
    # else:
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    #     topic1 = types.KeyboardButton('Космос')
    #     topic2 = types.KeyboardButton('Книги')
    #     markup.add(topic1, topic2)
    #     final_message = 'Ой, бро, что-то не то, нажми на кнопки ниже'
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
                        'А теперь можешь перейти ко второй теме, если ты ещё не решал её\n' \
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
    # else:
     #   markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
      #  topic1 = types.KeyboardButton('Космос')
       ##markup.add(topic1, topic2)
        #final_message = 'Ой, бро, что-то не то, нажми на кнопки ниже'

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


# @bot.message_handler(content_types=['text'])
# def books(message):
#     global markup, final_message
#     get_message_bot = message.text
#     if get_message_bot == 'Книги':
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
#         btn1 = types.KeyboardButton('Толстой Л.Н.')
#         btn2 = types.KeyboardButton('Шолохов М.А.')
#         btn3 = types.KeyboardButton('Сложеницын А.И')
#         markup.add(btn1, btn2, btn3)
#         final_message = 'Кому принадлежит произведение "Тихий Дон"?'
#     elif get_message_bot == 'Толстой Л.Н.' or get_message_bot == 'Сложеницын А.И':
#         final_message = 'Неверно :(\n' \
#                         'Прочитай, пожалуйста <a href="https://www.litres.ru/mihail-sholohov/tihiy-don/">' \
#                         'великое произведение</a>\n' \
#                         'И напиши снова /game'
#     else:
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
#         topic1 = types.KeyboardButton('Космос')
#         topic2 = types.KeyboardButton('Книги')
#         markup.add(topic1, topic2)
#         final_message = 'Ой, бро, что-то не то, нажми на кнопки ниже'
#
#     if get_message_bot == 'Шолохов М.А.':
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
#         btn1 = types.KeyboardButton('№1')
#         btn2 = types.KeyboardButton('№2')
#         btn3 = types.KeyboardButton('№3')
#         markup.add(btn1, btn2, btn3)
#         photo1 = open('photo1.jpg', 'rb')
#         bot.send_message(message.chat.id, text='№1')
#         bot.send_photo(message.chat.id, photo1)
#         photo2 = open('photo2.jfif', 'rb')
#         bot.send_message(message.chat.id, text='№2')
#         bot.send_photo(message.chat.id, photo2)
#         photo3 = open('photo3.jfif', 'rb')
#         bot.send_message(message.chat.id, text='№3')
#         bot.send_photo(message.chat.id, photo3)
#         final_message = 'На какой из картинки изображен Достовеский Ф.М.? '

# elif get_message_bot == '7' or get_message_bot == '8':
#     final_message = 'Неверно :(\n' \
#                     'Посмотри, пожалуйста эту <a href="https://postnauka.ru/tv/64056">' \
#                     'статью</a>\n' \
#                     'И напиши снова /game'
# if get_message_bot == '9':
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
#     btn1 = types.KeyboardButton('75')
#     btn2 = types.KeyboardButton('65')
#     btn3 = types.KeyboardButton('79')
#     markup.add(btn1, btn2, btn3)
#     final_message = 'Сколько спутников у Юпитера по состоянию 2018 года?'
# elif get_message_bot == '75' or get_message_bot == '65':
#     final_message = 'Неверно :(\n' \
#                     'Посмотри, пожалуйста эту <a href="https://starwalk.space/ru/news/jupiter-galilean-moons">' \
#                     'статью</a>\n' \
#                     'И напиши снова /game'
# if get_message_bot == '79':
#     final_message = '<b>Молодец, ты ответил на все вопросы верно!🔥</b>\n' \
#                     'А теперь можешь перейти ко второй теме, если ты ещё не решал её'
# bot.send_message(message.chat.id, text=final_message, reply_markup=markup, parse_mode='html')


# markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
# btn1 = types.KeyboardButton("👋 Поздороваться")
# btn2 = types.KeyboardButton("❓ Задать вопрос")
# markup.add(btn1, btn2)
# bot.send_message(message.chat.id,
#                  text="Привет, {0.first_name}! Я тестовый бот для твоей статьи для habr.com".format(
#                      message.from_user), reply_markup=markup)

# @bot.message_handler(content_types=['text'])
# def topics(message):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
#     topic1 = types.KeyboardButton('Космос')
#     topic2 = types.KeyboardButton('Книги')
#     markup.add(topic1, topic2)
#     bot.send_message(message.chat.id, 'Какая тема Quiz тебя интересует?', reply_markup=markup)

#
# @bot.message_handler()
# def website():
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
#     website = types.KeyboardButton('GitH11ub')
#     urlGit = types.InlineKeyboardMarkup()
#     urlGit.add(types.InlineKeyboardButton('Посетить веб-сайт лучшего человека', url='https://vk.com/ilsaffff'))
#     markup.add(website)

# создаём обработчика сообщения, команды типа /start и /help

# @bot.message_handler(commands=['start'])
# def commands(message):
#     mess = f'Привет, <b>{message.from_user.first_name} <u>{message.from_user.last_name}</u></b>'
#     bot.send_message(message.chat.id, mess, parse_mode='html')  # бот ответит на команды вопросом

# @bot.message_handler()
# def get_user_text(message):
#     if message.text == "Hello":
#         bot.send_message(message.chat.id, "И тебе привет", parse_mode='html')
#     elif message.text == "id":
#         bot.send_message(message.chat.id, f'Твой ID: <b>{message.from_user.id}</b>', parse_mode='html')
#     elif message.text == 'photo':
#         photo = open('ph.jpg', 'rb')
#         bot.send_photo(message.chat.id, photo)
#     elif message.text == 'Where does live Ilsaf?':
#         bot.send_location(message.chat.id, 60.021757, 30.388245)
# else:
#     bot.send_message(message.chat.id, 'Я тебя не понимаю :(', parse_mode='html')

# @bot.message_handler(content_types=['photo'])
# def get_user_photo(message):
#     bot.send_message(message.chat.id, 'Вау, крутое фото')

# @bot.message_handler(commands=['website'])
# def website(message):
#     markup = types.InlineKeyboardMarkup()
#     markup.add(types.InlineKeyboardButton('Посетить веб-сайт лучшего человека', url='https://vk.com/ilsaffff'))
#
#
# @bot.message_handler(commands=['help'])
# def website(message):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
#     website = types.KeyboardButton('Веб сайт')
#     start = types.KeyboardButton('Start')
#     markup.add(website, start)
#     bot.send_message(message.chat.id, 'Вау, крутое фото', reply_markup=markup)


bot.polling(none_stop=True)