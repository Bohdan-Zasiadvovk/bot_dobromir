from database import Database
import User
import json

class Order:
    DBcursor = None
    user = None
    order_details = {}

    def __init__(self, user_tg_id: str, db_cursor: Database, order_details=None):
        self.user_tg_id = user_tg_id
        self.DBcursor = db_cursor
        self.user = User(user_tg_id, db_cursor)

        order_dict = self.db_to_dict()

        self.id = order_dict['id']
        self.tg_id = order_dict['tg_id']
        self.order_details = order_dict['order_details']
        self.datetime = order_dict['datetime']
        self.status = order_dict['status']


    def db_to_dict(self):
        order_tuple = self.DBcursor.get_last_new_by_tg_id(self.tg_id)
        if not order_tuple:
            self.DBcursor.create_order(self.user_tg_id, self.order_details)
            order_tuple = self.DBcursor.get_last_new_by_tg_id(self.tg_id)
        order_list = list(order_tuple)
        order = {
            'id': order_list[0],
            'tg_id': order_list[1],
            'order_details': order_list[2],
            'datetime': order_list[3],
            'status': order_list[4],
        }
        return order

    def create_order(self):
        self.DBcursor.create_order()

    def get_order_details(self):
        return self.order_details

    def update_product(self, product_slug, count):
        if product_slug in self.order_details:
            self.order_details[product_slug] = count
            return True
        else:
            return False

    def add_product(self, product_slug):
        if product_slug not in self.order_details:
            self.order_details[product_slug] = 0
            return True
        else:
            return False

    def set_count(self, product_slug, count):
        if product_slug in self.order_details:
            self.order_details[product_slug] = count
            return True
        else:
            return False

    def delete_product(self, product_slug):
        if product_slug in self.order_details:
            del self.order_details[product_slug]
            return True
        else:
            return False

    def confirmed_order(self):
        self.status = "confirmed"
        return True

    def __del__(self):
        self.DBcursor.update_order(self.user_tg_id, json.dumps(self.order_details))