from classes.Database import Database
from classes.Validator import Validator
import json

val = Validator()

class User:
    DBcursor = None
    default_name = ""
    default_phone = ""
    default_username = ""

    def __init__(self, tg_id: str, db_cursor: Database, botObj=False, name="", phone="", username=""):
        self.botObj = botObj
        if tg_id == "5469111431":
            # doing something
            print("WARNING!!!!")
        if val.validate_text(tg_id):
            self.tg_id = tg_id
        else:
            self.botObj.send_message_admin(f"Помилка валідації tg_id: {tg_id} при ініціалізації User")
        if val.validate_text(name):
            self.default_name = name
        else:
            self.botObj.send_message_admin(f"Помилка валідації name: {name} при ініціалізації User")
        if val.validate_text(phone):
            self.default_phone = phone
        else:
            self.botObj.send_message_admin(f"Помилка валідації phone: {phone} при ініціалізації User")
        if val.validate_text(username):
            self.default_username = username
        else:
            self.botObj.send_message_admin(f"Помилка валідації username: {username} при ініціалізації User")

        self.DBcursor = db_cursor

        user_dict = self.db_to_dict()

        self.id = user_dict['id']
        self.name = user_dict['name']
        self.phone = user_dict['phone']
        self.username = user_dict['username']

    def __str__(self):
        user_dict = {
            "id": self.id,
            "tg_id": self.tg_id,
            "name": self.name,
            "phone": self.phone,
            "username": self.username
        }
        return json.dumps(user_dict, indent=4)

    def db_to_dict(self):
        user_tuple = self.DBcursor.get_user(self.tg_id)
        if not user_tuple:
            self.DBcursor.create_user(self.tg_id, self.default_name, self.default_phone, self.default_username)
            user_tuple = self.DBcursor.get_user(self.tg_id)
        user_list = list(user_tuple)
        user = {
            'id': user_list[0],
            'tg_id': user_list[1],
            'name': user_list[2],
            'phone': user_list[3],
            'username': user_list[4],
        }
        return user

    def update_user(self, name: str, username: str):
        self.name = name
        self.username = username

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def tg_id(self):
        return self._tg_id

    @tg_id.setter
    def tg_id(self, value):
        self._tg_id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        self._phone = value

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    def __del__(self):
        self.DBcursor.update_user(self.tg_id, self.name, self.username)
