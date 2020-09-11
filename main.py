import telebot
import config

class Processing:

    def __init__(self):
        pass

    @staticmethod
    def coord_idenify(message):
        try:
            lat, lot = [float(x) for x in message.split(', ')]
            return (lat, lot)
        except ValueError:
            return message

process = Processing()
bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    item1 = telebot.types.InlineKeyboardButton('Да, конечно!', callback_data='game_yes')
    item2 = telebot.types.InlineKeyboardButton('Нет, мне это не интересно.', callback_data='game_no')

    markup.add(item1, item2)

    bot.send_message(message.chat.id, f'Привет, <b>{message.from_user.first_name}</b>, меня зовут бот <b>Олег</b>! *Текст*.\nХочешь поиграть в игру? 🤠',
                     reply_markup=markup,
                     parse_mode='html')

@bot.message_handler(content_types=['text'])
def send_message(message):
    if message.chat.type == 'private':
        message_text = process.coord_idenify(message.text)

        if message.text == 'Прекрасно, идём дальше!\nВыбери один из вариантов продолжения игры: ':
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = telebot.types.KeyboardButton('Показать всех Олегов!')
            item2 = telebot.types.KeyboardButton('Показать все Арены!')
            item3 = telebot.types.KeyboardButton('Показать всё!')
            markup.add(item1, item2, item3)

            bot.send_message(message.chat.id, f'Что выберем, {message.from_user.first_name}?', reply_markup=markup)

        elif isinstance(message_text, tuple):
            lat, lon = message_text

            markup = telebot.types.InlineKeyboardMarkup(row_width=2)
            item1 = telebot.types.InlineKeyboardButton('Да', callback_data='yes_catch_oleg')
            item2 = telebot.types.InlineKeyboardButton('Нет', callback_data='no_catch_oleg')

            markup.add(item1, item2)
            bot.send_message(message.chat.id, f'Так-с, давай проверим:\nШирота = {lat}, Долгота = {lon}\nВсё верно?',
                             reply_markup=markup)

@bot.callback_query_handler(func=lambda cell: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'game_yes':
                markup = telebot.types.InlineKeyboardMarkup(row_width=4)
                item1 = telebot.types.InlineKeyboardButton('Поимка Олега! 🏃🏻', callback_data='catch_oleg')
                item2 = telebot.types.InlineKeyboardButton('Показать Арены! 🤼', callback_data='show_arena')
                item3 = telebot.types.InlineKeyboardButton('Показать Мешок! ‍💼 ', callback_data='show_bag')

                markup.add(item1, item2)
                markup.add(item3)

                bot.send_message(call.message.chat.id,
                                 'У нас есть <b>3</b> режима! Выбирай!',
                                 reply_markup=markup,
                                 parse_mode='html')

            elif call.data == 'game_no':
                bot.send_message(call.message.chat.id,
                                 'Тогда пока... 😥')

            elif call.data == 'catch_oleg':
                bot.send_message(call.message.chat.id, 'Отправь мне свои координаты <3.\nФормат: <Широта>, <Долгота>')

            elif call.data == 'yes_catch_oleg':
                bot.send_message(call.message.chat.id, 'Прекрасно, идём дальше!')

            elif call.data == 'no_catch_oleg':
                bot.send_message(call.message.chat.id, 'Так-с, введи координаты ещё раз.')

            elif call.data == 'show_arena':
                bot.send_message(call.message.chat.id, 'Итак, правила игры следующие: ')

            elif call.data == 'show_bag':
                bot.send_message(call.message.chat.id, 'Итак, правила игры следующие: ')



    except Exception as e:
        print(repr(e))


if __name__ == "__main__":
    bot.polling(none_stop=True)

# @bot.message_handler(commands=["start"])
# def start_message(message):
#     user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
#     user_markup.row("Курсы валют", "Новости")
#     bot.send_message(message.chat.id, "Добрый день", reply_markup=user_markup)
#
# @bot.message_handler(regexp="Курсы валют")
# def value_message(message):
#     keyboardV = telebot.types.InlineKeyboardMarkup()
#     kbv1 = telebot.types.InlineKeyboardButton(text="Доллар", callback_data="USD")
#     kbv2 = telebot.types.InlineKeyboardButton(text="Евро", callback_data="EUR")
#     kbv3 = telebot.types.InlineKeyboardButton(text="Фунт", callback_data="GBP")
#     keyboardV.add(kbv1, kbv2, kbv3)
#     bot.send_message(message.chat.id, "Выберите валюту: ", reply_markup=keyboardV)
#
#
# @bot.message_handler(regexp="Новости")
# def selectCounrty(message):
#     # Клавиатура выбора стран
#     keyboard = telebot.types.InlineKeyboardMarkup()
#     kb1 = telebot.types.InlineKeyboardButton(text="Россия", callback_data="country1")
#     kb2 = telebot.types.InlineKeyboardButton(text="Германия", callback_data="country2")
#     keyboard.add(kb1, kb2)
#     bot.send_message(message.chat.id, "Список стран: ", reply_markup=keyboard)
#
#
#
# @bot.callback_query_handler(func=lambda c:True)
# def inline(callback):
#     print(callback.data)
#
# bot.polling()

