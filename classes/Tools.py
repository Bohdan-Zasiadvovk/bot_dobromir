
class Tools:

    @staticmethod
    def get_key_by_value(dictionary, value):
        for key, val in dictionary.items():
            if val == value:
                return key
        return None  # Возвращаем None, если значение не найдено
