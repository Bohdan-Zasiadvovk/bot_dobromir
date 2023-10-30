from classes.Validator import Validator
import sqlite3
import json

val = Validator()

class Database:
    def __init__(self, db_name='bot_dobromir.db', botObj=False):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.botObj = botObj

    def create_user(self, tg_id, name, phone, username):
        if all(map(val.validate_text, [tg_id, name, phone, username])):
            self.cursor.execute('INSERT INTO users (tg_id, name, phone, username) VALUES (?, ?, ?, ?)',
                                (tg_id, name, phone, username))
            self.conn.commit()
        else:
            self.botObj.send_message_admin(f'Виникла помилка валідації при створенні користувача\n'
                                           f'Користувач: @{username}\n'
                                           f'Ім\'я: {name}\n'
                                           f'Телефон: {phone}\n'
                                           f'Tg_id: {tg_id}')
        return True

    def get_user(self, tg_id):
        if val.validate_text(tg_id):
            self.cursor.execute('SELECT * FROM users WHERE tg_id = ?', (tg_id,))
            return self.cursor.fetchone()

        else:
            self.botObj.send_message_admin(f'Виникла помилка валідації при отриманні користувача\n'
                                           f'Користувач:\n'
                                           f'Tg_id: {tg_id}')

# If user in database - returns user data
# if user is not in database (check with tg_id) - call function for create user
    def get_or_create_user(self, tg_id, name, phone, username):
        # validation input data
        if all(map(val.validate_text, [tg_id, name, phone, username])):
            user = self.get_user(tg_id)
            if user:
                return user
            else:
                self.create_user(tg_id, name, phone, username)
                return self.get_user(tg_id)
        else:
            self.botObj.send_message_admin(f'Виникла помилка валідації при створенні/отриманні користувача\n'
                                           f'Користувач: @{username}\n'
                                           f'Ім\'я: {name}\n'
                                           f'Телефон: {phone}\n'
                                           f'tg_id: {tg_id}')

    def update_user(self, tg_id, new_name=False, new_username=False):

        if val.validate_text(tg_id):
            if new_name and val.validate_text(new_name):
                self.cursor.execute('UPDATE users SET name = ? WHERE tg_id = ?', (new_name, tg_id))
                self.conn.commit()
            elif new_username and val.validate_text(new_username):
                self.cursor.execute('UPDATE users SET username = ? WHERE tg_id = ?', (new_username, tg_id))
                self.conn.commit()
            else:
                self.botObj.send_message_admin(f'Виникла помилка валідації при оновленні користувача\n'
                                               f'Користувач:\n'
                                               f'Нове ім\'я: {new_name}\n'
                                               f'Новий username: @{new_username}\n'
                                               f'Tg_id: {tg_id}')
        else:
            self.botObj.send_message_admin(f'Виникла помилка валідації при оновленні користувача\n'
                                           f'Користувач:\n'
                                           f'Tg_id: {tg_id}')
        return False

    def get_product(self, slug):
        if val.validate_text(slug):
            self.cursor.execute('SELECT * FROM products WHERE slug = ?', (slug,))
            return self.cursor.fetchone()
        else:
            self.botObj.send_message_admin(f'Виникла помилка при отриманні товару {slug}')

    def get_product_list(self):
        self.cursor.execute('SELECT * FROM products')
        return self.cursor.fetchall()

    def create_order(self, user_id, order_details, status='new'):
        if val.validate_number(user_id) and val.validate_dict(order_details):
            self.cursor.execute('INSERT INTO orders (user_id, order_details, status) VALUES (?, ?, ?)',
                                (user_id, json.dumps(order_details), status))
            self.conn.commit()
        else:
            self.botObj.send_message_admin(f'Виникла помилка валідації при створенні замовлення\n'
                                           f'Користувач:\n'
                                           f'Id: {user_id}\n'
                                           f'Деталі замовлення:\n{order_details}\n'
                                           f'Статус: {status}')
        return True

    def get_last_new_by_tg_id(self, tg_id):
        if val.validate_text(tg_id):
            self.cursor.execute('''
                SELECT o.* FROM orders o
                JOIN users u ON o.user_id = u.id
                WHERE u.tg_id = ? AND o.status = "new"
                ORDER BY o.datetime DESC LIMIT 1
            ''', (tg_id,))
            last_order = self.cursor.fetchone()

            if last_order:
                return last_order
            else:
                return False
        else:
            self.botObj.send_message_admin(f'Виникла помилка валідації при отриманні останнього замовлення зі статусом new\n'
                                           f'Користувач:\n'
                                           f'Tg_id: {tg_id}')

    def update_order(self, order_id, order_details, status):
        if val.validate_dict(order_details):
            self.cursor.execute('UPDATE orders SET order_details = ?, status = ? WHERE id = ?',
                                (json.dumps(order_details), status, order_id))
            self.conn.commit()
        else:
            self.botObj.send_message_admin(f'Виникла помилка валідації при оновленні замовлення\n'
                                           f'Користувач:\n'
                                           f'Id замовлення: {order_id}\n'
                                           f'Деталі замовлення:\n{order_details}\n'
                                           f'Статус: {status}')
        return True

    def set_status_confirmed(self, order_id):
        self.cursor.execute('UPDATE orders SET status = "confirmed" WHERE id = ?', (order_id,))
        self.conn.commit()
        return True

    def set_status_done(self, order_id):
        self.cursor.execute('UPDATE orders SET status = "done" WHERE id = ?', (order_id,))
        self.conn.commit()
        return True

    def set_status_deleted(self, order_id):
        self.cursor.execute('UPDATE orders SET status = "deleted" WHERE id = ?', (order_id,))
        self.conn.commit()
        return True

    def close(self):
        self.conn.close()

    def __del__(self):
        self.conn.close()
