import random

class Processing:

    def __init__(self):
        pass

    @staticmethod
    def coord_idenify(message):
        try:
            lat, lot = [float(x) for x in message.replace(' ', '').split(',')]
            return (lat, lot)
        except ValueError:
            return message

    @staticmethod
    def cashback_value(seed):
        random.seed(seed)
        return random.randint(4, 9)

    def get_fact(self, seed=None):
        if seed:
            random.seed(seed)

        key = random.randint(1, 2)
        if key == 1:
            text = f'\nКстати, совершив покупку в этом месте, ты сможешь получить кешбэк <b>{self.cashback_value(seed)}</b>%.'
        elif key == 2:
            text = f'Интересный факт: За последний месяц ты тут потратил {random.randint(200, 2000)} рублей!'

        return text

    @staticmethod
    def find_stores():
        distances_store = [300, 600, 800, 1000]

        result = {}
        text = f'Ого! Рядом есть 4 Олега(-ов).'
        for index, value in enumerate(distances_store):
            index += 1
            add_text = f'\n{index}) {value} метров.'
            text += add_text

            result[index] = value

        text += '\nНу что, куда пойдём? Введи номер!'
        return text, result


        # random.seed(seed)
        #
        # stores = [
        #     'Пятёрочка',
        #     'Перекрёсток',
        #     'Магнит',
        #     'Бристоль',
        #     'BILLA',
        #     'ВкусВилл',
        #     'Азбука Вкуса'
        # ]
        #
        # group_of_items = stores
        # num_to_select = random.randint(1, len(stores))
        # list_of_random_items = random.sample(group_of_items, num_to_select)
        #
        # distances = list(range(100, 1000, 100))
        #
        # result = {}
        # text = f'Ого! Рядом есть {num_to_select} Олега(-ов).'
        # for index, value in enumerate(list_of_random_items):
        #     index += 1
        #     distance = random.sample(distances, 1)
        #     add_text = f'\n{index}) {value} ({distance[0]} метров)'
        #     text += add_text
        #
        #     result[index] = value
        #
        # text += '\nНу что, куда пойдём? Введи номер!'
        #
        # return text, result

facts = [
"""<b>Признаки финансовой пирамиды</b>:
- обещание высокой доходности, в несколько раз превышающей рыночный уровень;
- отсутствие собственных основных средств и других дорогостоящих активов
- отсутствие лицензии ФСФР России или Банка России на осуществление деятельности по привлечению денежных средств
- массированная реклама в СМИ, сети Интернет с обещанием высокой доходности
- отсутствие какой-либо информации о финансовом положении организации и стратегии инвестирования\n
Почитать больше можно тут: https://journal.tinkoff.ru/kb/piramida/""",

"""<b>Факт</b>\n
Если вы решили взять кредит, в первую очередь следует обратить внимание на:
На полную стоимость кредита
На условия возврата кредита досрочно
На величину процентной ставки
На ежемесячный платеж

Ещё больше по ссылке: https://journal.tinkoff.ru/selected/credit/""",
"""<b>Факт</b>\n
Чтобы быть уверенным в безопасности имеющихся на счету банковской карты средств:
НИКОГДА НЕ храните записанный PIN-код вместе с картой
НИКОГДА НЕ сообщайте свой PIN-код сотруднику банка по телефону по его запросу
НИКОГДА НЕ вводите данные карты на интернет-сайтах без защищенного соединения (https)
НИКОГДА НЕ позволяйте официанту в ресторане или кафе производить действия с вашей картой вне вашего поля зрения
Немедленно заблокируйте карту, в случае её потери\n
Узнать больше можно тут: https://www.tinkoff.ru/secure/""",

"""<b>Факт</b>\n
Для защиты своих прав как потребителя финансовых услуг можно обращаться с жалобой/претензией в:
Роспотребнадзор
Общественный примиритель на финансовом рынке (финансовый омбудсмен)
Общества защиты прав потребителей
Центральный Банк Российской Федерации
Суд

Права потребителя в магазине: https://journal.tinkoff.ru/prava/potrebitel/"""
]
