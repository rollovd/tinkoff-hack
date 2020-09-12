import telebot
import config
from dictionary_answer import dictionary_answer
from Processing import Processing

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
            key = call.data
            text = dictionary_answer[key]

            if key == 'game_yes':
                markup = telebot.types.InlineKeyboardMarkup(row_width=4)
                item1 = telebot.types.InlineKeyboardButton('Поимка Олега! 🏃🏻', callback_data='catch_oleg')
                item2 = telebot.types.InlineKeyboardButton('Показать Арены! 🤼', callback_data='show_arena')
                item3 = telebot.types.InlineKeyboardButton('Показать Мешок! ‍💼 ', callback_data='show_bag')

                markup.add(item1, item2)
                markup.add(item3)

                bot.send_message(call.message.chat.id,
                                 text,
                                 reply_markup=markup,
                                 parse_mode='html')
            else:
                bot.send_message(call.message.chat.id, text)

    except Exception as e:
        print(repr(e))

if __name__ == "__main__":
    bot.polling(none_stop=True)

