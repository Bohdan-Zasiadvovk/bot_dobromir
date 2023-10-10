import sqlite3
import json
from validator import *

val = Validator()

class Database:
    def __init__(self, db_name='bot_dobromir.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_user(self, tg_id, name, phone, username):
        self.cursor.execute('INSERT INTO users (tg_id, name, phone, username) VALUES (?, ?, ?, ?)',
                            (tg_id, name, phone, username))
        self.conn.commit()

    def get_user(self, tg_id):
        self.cursor.execute('SELECT * FROM users WHERE tg_id = ?', (tg_id,))
        return self.cursor.fetchone()

# If user in database - returns user data
# if user is not in database (check with tg_id) - call function for create user
    def get_or_create_user(self, tg_id, name, phone, username):
        # validation input data
        if val.validate_number(tg_id) & val.validate_text(name) & val.validate_number(phone) & val.validate_text(username):
            user = self.get_user(tg_id)
            if user:
                return user
            else:
                self.create_user(tg_id, name, phone, username)
                return self.get_user(tg_id)
        else:
            # send error to admin
            pass

    def update_user(self, tg_id, new_username):
        if val.validate_text(new_username):
            self.cursor.execute('UPDATE users SET username = ? WHERE tg_id = ?', (new_username, tg_id))
            self.conn.commit()
        else:
            # send error to admin
            pass

    def get_product(self, slug):
        self.cursor.execute('SELECT * FROM products WHERE slug = ?', (slug,))
        return self.cursor.fetchone()

    def get_product_list(self):
        self.cursor.execute('SELECT * FROM products')
        return self.cursor.fetchall()

    def create_order(self, user_id, order_details, status='new'):
        if val.validate_dict(order_details):
            self.cursor.execute('INSERT INTO orders (user_id, order_details, status) VALUES (?, ?, ?)',
                                (user_id, json.dumps(order_details), status))
            self.conn.commit()
        else:
            # send error to admin
            pass

# need test
    def get_last_new_by_tg_id(self, tg_id):
        # Get user_id from users
        self.cursor.execute('SELECT user_id FROM users WHERE tg_id = ?', (tg_id,))
        user_id = self.cursor.fetchone()

        self.cursor.execute('SELECT * FROM orders WHERE user_id = ? AND status = "new" ORDER BY datetime DESC LIMIT 1', (user_id,))
        return self.cursor.fetchone()

    def update_order(self, order_id, order_details):
        if val.validate_dict(order_details):
            self.cursor.execute('UPDATE orders SET order_details = ? WHERE id = ?', (json.dumps(order_details), order_id))
            self.conn.commit()
        else:
            # send error to admin
            pass

    def set_status_confirmed(self, order_id):
        self.cursor.execute('UPDATE orders SET status = "confirmed" WHERE id = ?', (order_id,))
        self.conn.commit()

    def set_status_done(self, order_id):
        self.cursor.execute('UPDATE orders SET status = "done" WHERE id = ?', (order_id,))
        self.conn.commit()

    def set_status_deleted(self, order_id):
        self.cursor.execute('UPDATE orders SET status = "deleted" WHERE id = ?', (order_id,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
