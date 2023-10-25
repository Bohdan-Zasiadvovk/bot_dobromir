import telebot
from telebot import types
from classes.Database import Database
from classes.Order import Order
from classes.Product import Product
from classes.User import User
from classes.Validator import Validator
from classes.Tools import Tools
# bot_id_in_tg : 5469111431

class TelegramBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.database_filename = "bot_dobromir.db"
        self.validator = Validator()

        # Initialize handlers
        self.initialize_handlers()

    def initialize_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            # Request phone number
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            item = types.KeyboardButton("Надіслати номер", request_contact=True)
            markup.add(item)
            self.bot.send_message(message.chat.id, "Аби ми могли з Вами зв'язатися для уточнення замовлення, "
                                                   "будь ласка, поділіться номером телефону. "
                                                   "Для цього натисніть кнопку нижче ",
                                                    reply_markup=markup)

        @self.bot.message_handler(content_types=['contact'])
        def handle_contact(message):
            # Create or get a user
            username = message.from_user.username if message.from_user.username else ""
            phone = message.contact.phone_number if message.contact.phone_number else ""
            tg_id = message.from_user.id
            name = message.chat.first_name if message.chat.first_name else ""
            user = User(str(tg_id), Database(self.database_filename, self), name, phone, username)
            self.send_product_selection(message)

        @self.bot.message_handler(content_types=['text'])
        def handle_text(message):
            try:
                count_of_product = int(Tools.get_count_from_str(message.text))
            except BaseException:
                count_of_product = ' ss '
            if message.text == "Нове замовлення":
                self.send_product_selection(message)
            elif self.validator.validate_number(count_of_product):
                count = int(message.text)
                # Update the product count in the current order
                order = Order(str(message.from_user.id), Database(self.database_filename, self))
                if order:
                    product = Tools.get_key_by_value(order.get_order_details(), 0)
                    order.set_count(product, count)
                self.send_additional_product_selection(message)

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            chat_id = str(call.message.chat.id)
            if call.data == "finish_order":
                # Finish the order and notify the admin
                order = Order(chat_id, Database(self.database_filename, self))
                order.confirmed_order()
                self.notify_admin(chat_id)
                self.bot.send_message(chat_id,
                                      "Дуже дякую за ваше замовлення, з вами дуже скоро зв'яжеться адмін для уточнень данних та відправки вам вашого замовлення")
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                item_new_order = types.KeyboardButton("Нове замовлення")
                markup.add(item_new_order)
                self.bot.send_message(chat_id,
                                      "Ваше замовлення прийнято. Якщо ви хочете зробити нове замовлення, натисніть кнопку \"Нове замовлення\".",
                                      reply_markup=markup)
            else:
                # Handle product selection and additional product selection
                product_slug = call.data.replace("_additional", "")
                product = Product(product_slug, Database(self.database_filename, self))
                if product:
                    order = Order(chat_id, Database(self.database_filename, self))

                    if product.slug in order.get_order_details():
                        old_count = order.get_order_details()[product.slug]
                        order.update_product(product.slug, 0)
                        self.bot.send_message(chat_id,
                                              f"Ви обрали {product.name}. Ви хочете змінити замовлення. "
                                              f"Спочатку Ви обрали {old_count} пакетів."
                                              f"Скільки пакетів {product.name} Ви хочете замовити?"
                                              f"Будь ласка, напишіть число.")
                    else:
                        order.add_product(product.slug)
                        self.bot.send_message(chat_id,
                                              f"Ви обрали {product.name}. "
                                              f"Скільки пакетів {product.name} Ви хочете замовити?"
                                              f"Будь ласка, напишіть число.")

    def send_product_selection(self, message):
        markup = types.InlineKeyboardMarkup(row_width=2)
        products = Product.get_all_products(Database(self.database_filename, self))
        for product in products:
            item = types.InlineKeyboardButton(product.name, callback_data=product.slug)
            markup.add(item)
        self.bot.send_message(message.chat.id, "Оберіть продукт:", reply_markup=markup)

        # Create an empty order for the user
        order = Order(str(message.from_user.id), Database(self.database_filename, self))
        # Database(self.database_filename, self).create_order(order)

    def send_additional_product_selection(self, message):
        markup = types.InlineKeyboardMarkup(row_width=2)
        products = Product.get_all_products(Database(self.database_filename, self))
        for product in products:
            item = types.InlineKeyboardButton("Так, хочу " + product.name, callback_data=product.slug + "_additional")
            markup.add(item)
        item_finish = types.InlineKeyboardButton("Ні, дякую, це все", callback_data="finish_order")
        markup.add(item_finish)
        self.bot.send_message(message.chat.id, "Чи бажаєте додати щось ще?", reply_markup=markup)

    def notify_admin(self, user_tg_id):
        order = Order(user_tg_id, Database(self.database_filename, self))
        if order:
            user = User(user_tg_id, Database(self.database_filename, self))
            if user:
                admin_message = f"Надійшло нове замовлення від {user.name}. Tg: @{user.username}\n(телефон: {user.phone}):\n"
                for product, count in order.get_order_details().items():
                    ProductObj = Product(product, Database(self.database_filename, self))
                    admin_message += f"{ProductObj.name}: {count}\n"
                # TODO: Replace ADMIN_CHAT_ID with the actual chat ID of the admin
                self.bot.send_message(321107998, admin_message)

    def send_message_admin(self, message):
        self.bot.send_message(321107998, message)


    def start_polling(self):
        self.bot.polling(none_stop=True)

