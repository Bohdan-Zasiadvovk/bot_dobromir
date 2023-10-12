from bot_dobromir.database import Database


class User:
    DBcursor = None

    def __init__(self, tg_id: str, db_cursor: Database):
        self.tg_id = tg_id
        self.DBcursor = db_cursor

        user_dict = self.db_to_dict()

        self.id = user_dict['id']
        self.name = user_dict['name']
        self.phone = user_dict['phone']
        self.username = user_dict['username']

    def db_to_dict(self):
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
