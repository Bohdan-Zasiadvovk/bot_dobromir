class Validator:

    @staticmethod
    def validate_text(text):
        if isinstance(text, str):
            return True
        return False

    @staticmethod
    def validate_number(num):
        if isinstance(num, int):
            return True
        return False

    @staticmethod
    def validate_dict(value):
        if isinstance(value, dict):
            return True
        return False
