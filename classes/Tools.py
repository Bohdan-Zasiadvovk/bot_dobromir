
class Tools:

    @staticmethod
    def get_key_by_value(dictionary, value):
        for key, val in dictionary.items():
            if val == value:
                return key
        return None  # Возвращаем None, если значение не найдено

    @staticmethod
    def get_count_from_str(text):
        num_str = ''
        found_number = False
        for char in text:
            if char.isdigit():
                num_str += char
                found_number = True
            elif found_number:
                # Якщо ми знайшли число і потрапили на не-цифровий символ, зупиняємо пошук
                break
        # Повертаємо число якщо знайдено, в іншому випадку None
        return int(num_str) if num_str else None
