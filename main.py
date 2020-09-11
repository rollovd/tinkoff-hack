import telebot
import config

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton('хай')
    item2 = telebot.types.KeyboardButton('Привет')
    markup.add(item1, item2)

    bot.send_message(message.chat.id, 'Хеллоу!', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def send_message(message):
    if message.chat.type == 'private':
        if message.text == 'хай':
            bot.send_message(message.chat.id, str(5))

        elif message.text == 'Привет':
            bot.send_message(message.chat.id, 'Гуд!')

if __name__ == "__main__":
    bot.polling(none_stop=True)

