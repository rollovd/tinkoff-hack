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