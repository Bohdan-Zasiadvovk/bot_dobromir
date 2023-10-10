class Validator:

    @staticmethod
    def validate_text(text):
        if isinstance(text, str):
            return text
        return False

    @staticmethod
    def validate_number(num):
        if isinstance(num, int):
            return num
        return False

    @staticmethod
    def validate_dict(value):
        if isinstance(value, dict):
            return value
        return False
