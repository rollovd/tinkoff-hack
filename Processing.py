import random

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

    @staticmethod
    def find_stores(seed):
        random.seed(seed)

        stores = [
            'Пятёрочка',
            'Перекрёсток',
            'Магнит',
            'Бристоль',
            'BILLA',
            'ВкусВилл',
            'Азбука Вкуса'
        ]

        group_of_items = stores
        num_to_select = random.randint(1, len(stores))
        list_of_random_items = random.sample(group_of_items, num_to_select)

        distances = list(range(100, 1000, 100))

        result = {}
        text = f'Ого! Рядом есть {num_to_select} Олега(-ов).'
        for index, value in enumerate(list_of_random_items):
            index += 1
            distance = random.sample(distances, 1)
            add_text = f'\n{index}) {value} ({distance[0]} метров)'
            text += add_text

            result[index] = value

        text += '\nНу что, куда пойдём? Введи номер!'

        return text, result
