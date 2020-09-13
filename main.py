import telebot
import config
import random
import geocoder
import Processing
import time
import questions

process = Processing.Processing()
bot = telebot.TeleBot(config.TOKEN)

leaderboard = {'Jamil': 20, 'Dima': 11, 'Maria': 15, 'Kirill': 5, 'lamoureux': 9}

saved_facts = []
arenas = 3

quotes = [
    (
        'Прогресс приходит к тем, кто тренируется изо дня в день. Полагающие на секретные техники ни к чему не придут.',
        'Морихэй Уэсиба'),
    (
        'Причина моего провала очевидна: я мало тренировался. И кроме того, я мало тренировался. И еще — я мало тренировался. Это если так, вкратце.',
        'Харуки Мураками'),
    (
        'Разум всегда сдается первым, не тело. Секрет в том, чтобы заставить твой разум работать на тебя, а не против тебя.',
        'Арнольд Шварценеггер')
]

@bot.message_handler(commands=['start'])
def start_command(message):
    global my_name

    img = open('images\oleggo.jpg', 'rb')
    bot.send_photo(message.chat.id, img)

    my_name = message.from_user.first_name

    bot.send_message(message.chat.id, f'Привет, <b>{my_name}</b>, меня зовут бот <b>Олег</b>!'
                                          f' Я голосовой помощник Тинькофф. Если хочешь, я могу стать и твоим помощником в финансовой сфере!'
                                          f' Я помогу тебе повысить твою финансовую грамотность, узнать об акциях многих магазинов и в целом расширить свой кругозор!'
                                          f' Соревнуйся в знаниях с другими пользователями, занимайся спортом и экономь, играя в OlegGo!.'
                                          f'\nХочешь поиграть в игру? 🤠',
                         parse_mode='html')

    text_info = f'Ты можешь воспользоваться любой из следующих команд:\n' \
                f'1) /game - данная команда предложит тебе сыграть в OlegGo;\n' \
                f'2) /saved_facts - данная команда покажет тебе список интересных финансовых фактов;\n' \
                f'3) /shop - данная команда позволит тебе пошопиться;\n' \
                f'4) /leaderboard - здесь ты можешь посмотреть на\n'

    bot.send_message(message.chat.id, text_info)

@bot.message_handler(commands=['game'])
def game_command(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=4)
    item1 = telebot.types.InlineKeyboardButton('Играть! ✌🏼', callback_data='play')
    item2 = telebot.types.InlineKeyboardButton('Показать Арены! 🤼', callback_data='show_arena')
    markup.add(item1)
    markup.add(item2)

    bot.send_message(message.chat.id, f'Во что хочешь сыграть, {message.from_user.first_name}?',
                     reply_markup=markup)


@bot.message_handler(commands=['saved_facts'])
def game_command(message):

    if not saved_facts:
        header = 'У тебя пока что нет интересных фактов :(\nИграй в OlegGo и узнавай много нового!'

    else:
        header = '<b>Saved facts</b>\n\n'
        for num_fact, fact in enumerate(list(set(saved_facts))):
            row_text = f'{num_fact+1}) {fact}.\n\n'
            header += row_text

    bot.send_message(message.chat.id, header,
                     parse_mode='html')

@bot.message_handler(commands=['shop'])
def game_command(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=4)
    item1 = telebot.types.InlineKeyboardButton('Купить шаги!', callback_data='buy_steps')
    item2 = telebot.types.InlineKeyboardButton('Купить подсказки!', callback_data='buy_hints')
    markup.add(item1)
    markup.add(item2)

    bot.send_message(message.chat.id, f'Что хочешь приобрести?',
                     reply_markup=markup)

@bot.message_handler(commands=['leaderboard'])
def game_command(message):
    sort_leaderboard = {k: v for k, v in sorted(leaderboard.items(), key=lambda item: item[1], reverse=True)}
    header = '<b>Leaderboard</b>\n\n'

    for place, (nick, score) in enumerate(sort_leaderboard.items()):
        row_text = f'{place + 1} place. Nick: <b>{nick}</b>, Score: <b>{score}</b>\n\n'
        header += row_text

    bot.send_message(message.chat.id, header,
                      parse_mode='html')

@bot.callback_query_handler(func=lambda cell: True)
def callback_inline(call):
    try:
        if call.message:
            callback_data = call.data

            if callback_data == 'show_arena':
                if not arenas:
                    text = 'К сожалению, Вы не сможете потренироваться, так как у Вас <b>нет</b> захваченных арен :(\n' \
                           'Нажмите на /game, чтобы вернуться в меню выбора.'
                    bot.send_message(call.message.chat.id, text, parse_mode='html')

                else:
                    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
                    item1 = telebot.types.InlineKeyboardButton('Да', callback_data='training')
                    item2 = telebot.types.InlineKeyboardButton('Нет', callback_data='to_game')
                    markup.add(item1)
                    markup.add(item2)

                    text = f'А вы не промах! Вы захватили {arenas} арену(ы)! Желаете потренироваться?'
                    bot.send_message(call.message.chat.id, text, reply_markup=markup)

            elif callback_data == 'buy_steps':
                bot.send_message(call.message.chat.id, f'Это демо-вариант. Функционал пока не подключен.\n'
                                                       f'Чтобы вернуться, нажмите на /game')

            elif callback_data == 'buy_hints':
                bot.send_message(call.message.chat.id, f'Это демо-вариант. Функционал пока не подключен.\n'
                                                       f'Чтобы вернуться, нажмите на /game')

            elif callback_data == 'to_game':
                markup = telebot.types.InlineKeyboardMarkup(row_width=4)
                item1 = telebot.types.InlineKeyboardButton('Да', callback_data='play')
                item2 = telebot.types.InlineKeyboardButton('Нет', callback_data='bye-bye')
                markup.add(item1)
                markup.add(item2)

                bot.send_message(call.message.chat.id, f'Тогда поиграем?',
                                 reply_markup=markup)

            elif callback_data == 'play':
                markup = telebot.types.InlineKeyboardMarkup(row_width=4)
                item1 = telebot.types.InlineKeyboardButton('Половим Олега! 🏃🏼', callback_data='catch_oleg')
                item2 = telebot.types.InlineKeyboardButton('Соревнование на Аренах! 💪', callback_data='arena_play')
                markup.add(item1)
                markup.add(item2)

                bot.send_message(call.message.chat.id, f'Поймаем Олега или посоревнуемся?',
                                 reply_markup=markup)

            elif callback_data == 'arena_play':
                bot.send_message(call.message.chat.id, f'Так-с, определяю твою геолокацию...')

                coords = geocoder.ip('me')
                bot.send_message(call.message.chat.id,
                                 f'Ага, я тебя нашёл! Вот твои координаты: {", ".join([str(x) for x in coords.latlng])}')

                bot.send_message(call.message.chat.id,
                                 f'Ищу ближайшие Арены...')
                time.sleep(1.5)

                markup = telebot.types.InlineKeyboardMarkup(row_width=4)
                item1 = telebot.types.InlineKeyboardButton('Да', callback_data='yes_capture_arena')
                item2 = telebot.types.InlineKeyboardButton('Нет', callback_data='no_capture_arena')
                markup.add(item1)
                markup.add(item2)
                bot.send_message(call.message.chat.id, 'Так-с, рядом с тобой есть одна Арена. Хочешь её захватить?',reply_markup=markup)

            elif callback_data == 'no_capture_arena':
                bot.send_message(call.message.chat.id, 'Чтобы вернуться в начало игры, нажми на /game')

            elif callback_data == 'quiz':
                global correct_quiz_answers
                correct_quiz_answers = 0

                quote_author = random.choice(quotes)

                quote = quote_author[0]
                author = quote_author[1]

                training_dict = questions.questions['playing']
                question_keys = random.sample(training_dict.keys(), len(training_dict))

                text = f"Как говорил {author}: '{quote}'\n\nМотивирует? Тогда начнём наш тест!\n\nПриготовьтесь, будет {len(training_dict)} вопроса. На один вопрос даётся 10 секунд."
                bot.send_message(call.message.chat.id, text)

                time.sleep(7)
                for key in question_keys:
                    global current_quiz_answer
                    global quiz_link

                    info = training_dict[key]
                    question = info['question']
                    answers = info['answers']
                    current_quiz_answer = info['correct_answer']
                    quiz_link = info['link']

                    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
                    for i in range(info['quantity_answers']):
                        markup.add(telebot.types.KeyboardButton('Вариант: ' + str(i + 1)))

                    text = question + answers + '\n\nВыберите номер ответа!'
                    bot.send_message(call.message.chat.id, text, reply_markup=markup)
                    time.sleep(10)

                bot.send_message(call.message.chat.id,
                                 f'Ты ответил правильно на {correct_quiz_answers}/{len(training_dict)} вопросов.\n'
                                 f'Возвращайся через час за новым тестом!', reply_markup=markup)

                try:
                    leaderboard[my_name] += correct_quiz_answers
                except KeyError:
                    leaderboard[my_name] = correct_quiz_answers

                del quiz_link
                del current_quiz_answer
                bot.send_message(call.message.chat.id, 'Чтобы вернуться в начало игры, нажми на /game')

            elif callback_data == 'yes_capture_arena':
                markup = telebot.types.InlineKeyboardMarkup(row_width=4)
                item1 = telebot.types.InlineKeyboardButton('Поехали!', callback_data='quiz')
                markup.add(item1)

                bot.send_message(call.message.chat.id, 'Чтобы захватить Арену, ты должен победить её владельца в финансовой викторине!\nЯ задам тебе 5 вопросов, на каждый их них у тебя будет 15 секунд на размышление.\nЕсли дашь больше ответов, чем текущий владелец - Арена твоя!\nУдачи! 🦄', reply_markup=markup)

            elif callback_data == 'catch_oleg':
                bot.send_message(call.message.chat.id, f'Так-с, определяю твою геолокацию...')

                coords = geocoder.ip('me')
                bot.send_message(call.message.chat.id, f'Ага, я тебя нашёл! Вот твои координаты: {", ".join([str(x) for x in coords.latlng])}')

                bot.send_message(call.message.chat.id,
                                 f'Ищу ближайших Олегов...')
                time.sleep(1.5)
                img = open('images\oleges.png', 'rb')
                bot.send_photo(call.message.chat.id, img)

                bot.send_message(call.message.chat.id, process.find_stores())

            elif callback_data == 'bye-bye':
                bot.send_message(call.message.chat.id, f'Тогда поиграем в другой раз! Не забывай, что у тебя есть ещё несколько доступных команд:\n'
                                                       f'1) /saved_facts\n2) /shop\n3) /leaderboard')

            elif callback_data == 'change_place':
                bot.send_message(call.message.chat.id, process.find_stores())

            elif callback_data == 'not_add_fact':
                bot.send_message(call.message.chat.id, 'Чтобы вернуться в начало игры, нажми на /game')

            elif callback_data == 'get_destination':
                global text_fact

                img = open(r'images\find_oleg.png', 'rb')
                bot.send_photo(call.message.chat.id, img)
                time.sleep(1.5)
                bot.send_message(call.message.chat.id, 'Молодец, ты нашёл Олега! За это ты получаешь +1 к рейтингу и одну монету.')

                text_fact = random.choice(Processing.facts)
                bot.send_message(call.message.chat.id,
                                 f'Кстати, ты нашёл Олега в "Перекрёстке", где каждый клиент банка Тинькофф может получить {random.randint(3, 9)}% кешбэка на первую покупку от 1000 рублей.\n\n')
                time.sleep(1)

                markup = telebot.types.InlineKeyboardMarkup(row_width=4)
                item1 = telebot.types.InlineKeyboardButton('Да!', callback_data='add_fact')
                item2 = telebot.types.InlineKeyboardButton('Нет, спасибо.', callback_data='not_add_fact')
                markup.add(item1)
                markup.add(item2)

                bot.send_message(call.message.chat.id, f'Интересный факт от Олега:\n{text_fact}', parse_mode='html')
                bot.send_message(call.message.chat.id, f'Добавить факт в сохранённые?', reply_markup=markup)

            elif callback_data == 'add_fact':
                saved_facts.append(text_fact)
                bot.send_message(call.message.chat.id,
                                 'Факт успешно сохранён! Информацию можно найти в /saved_facts 👍')
                bot.send_message(call.message.chat.id, 'Чтобы вернуться в начало игры, нажми на /game')

            elif callback_data == 'training':
                global correct_train_answers
                correct_train_answers = 0

                quote_author = random.choice(quotes)

                quote = quote_author[0]
                author = quote_author[1]

                training_dict = questions.questions['training']
                question_keys = random.sample(training_dict.keys(), len(training_dict))

                text = f"Как говорил {author}: '{quote}'\n\nМотивирует? Тогда начнём наш тест!\n\nПриготовьтесь, будет {len(training_dict)} вопроса. На один вопрос даётся 10 секунд."
                bot.send_message(call.message.chat.id, text)

                time.sleep(7)
                for key in question_keys:
                    global current_answer

                    info = training_dict[key]
                    question = info['question']
                    answers = info['answers']
                    current_answer = info['correct_answer']

                    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
                    for i in range(info['quantity_answers']):
                        markup.add(telebot.types.KeyboardButton('Ответ: ' + str(i+1)))

                    text = question + answers + '\n\nВыберите номер ответа!'
                    bot.send_message(call.message.chat.id, text, reply_markup=markup)
                    time.sleep(13)

                bot.send_message(call.message.chat.id, f'Ты ответил правильно на {correct_train_answers}/{len(training_dict)} вопросов.\n'
                                                       f'Возвращайся через час за новым тестом!', reply_markup=markup)

                del current_answer
                bot.send_message(call.message.chat.id, 'Чтобы вернуться в начало игры, нажми на /game')

    except Exception as e:
        print(repr(e))

@bot.message_handler(content_types=['text'])
def send_message(message):
    if 'Ответ' in message.text:
        global correct_train_answers
        value = int(message.text.split(' ')[1])

        try:
            if value == int(current_answer):
                bot.send_message(message.chat.id, 'Молодец! Всё верно!')
                correct_train_answers += 1
            else:
                bot.send_message(message.chat.id, f'Не-а! Правильный ответ под номером {current_answer}.')

        except NameError:
            pass

    elif 'Вариант' in message.text:
        global correct_quiz_answers
        value = int(message.text.split(' ')[1])

        try:
            if value == int(current_quiz_answer):
                text = 'Молодец! Всё верно!'
                if quiz_link:
                    text += f'\nПодробнее ты можешь почитать тут: {quiz_link}'

                bot.send_message(message.chat.id, text)
                correct_quiz_answers += 1
            else:
                text = f'Не-а! Правильный ответ под номером {current_quiz_answer}.'
                if quiz_link:
                    text += f'\nПодробнее ты можешь почитать тут: {quiz_link}'

                bot.send_message(message.chat.id, text)

        except NameError:
            pass

    elif isinstance(message.text, str) and len(message.text) <= 3:
        try:

            store_dict = {
                1: 'Перекрёсток',
                2: 'Магнит',
                3: 'Пятёрочка',
                4: 'BILLA'
            }

            markup = telebot.types.InlineKeyboardMarkup(row_width=5)
            item1 = telebot.types.InlineKeyboardButton('Я на месте! 👌🏻', callback_data='get_destination')
            item2 = telebot.types.InlineKeyboardButton('Хочу в другое место! 🔄', callback_data='change_place')

            markup.add(item1)
            markup.add(item2)

            _ = store_dict[int(message.text)]

            img = open(f'images\oleg_{int(message.text)}.jpg', 'rb')
            bot.send_photo(message.chat.id, img)

            bot.send_message(message.chat.id, 'Помчали?', parse_mode='html',
                             reply_markup=markup
                             )

        except KeyError:
            bot.send_message(message.chat.id, f'Дружок, я не вижу такой цифры... Попробуй ещё раз!😉')

if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)

    except Exception as e:
        time.sleep(5)



