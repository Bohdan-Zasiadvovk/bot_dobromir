import telebot
from telebot import types
from classes.Database import Database
from classes.Order import Order
from classes.Product import Product
from classes.User import User
from classes.Validator import Validator

# bot_id_in_tg : 5469111431

class TelegramBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.database_filename = "bot_dobromir.db"
        self.validator = Validator()
        self.current_orders = {}  # To keep track of the current orders

        # Initialize handlers
        self.initialize_handlers()

    def initialize_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            # Request phone number
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            item = types.KeyboardButton("Share phone number", request_contact=True)
            markup.add(item)
            self.bot.send_message(message.chat.id, "test", reply_markup=markup)

        @self.bot.message_handler(content_types=['contact'])
        def handle_contact(message):
            # Create or get a user
            username = message.from_user.username
            phone = message.contact.phone_number
            tg_id = message.from_user.id
            # print(message.from_user.id)
            # print(message)
            name = message.chat.first_name
            user = User(str(tg_id), Database(self.database_filename), name, phone, username)
            # self.database.get_or_create_user(user)
            self.send_product_selection(message)

        @self.bot.message_handler(content_types=['text'])
        def handle_text(message):
            # print("test")
            # print(message.text)
            try:
                count_of_product = int(message.text)
            except BaseException:
                print("not count")
                count_of_product = ' ss '
            if message.text == "Нове замовлення":
                self.send_product_selection(message)
            elif self.validator.validate_number(count_of_product):
                print("test")
                count = int(message.text)
                # Update the product count in the current order
                order = Order(str(message.from_user.id), Database(self.database_filename))
                # order = self.current_orders.get(message.from_user.id)
                if order:
                    print(order.get_order_details())
                    # TODO: BUG
                    product = list(order.get_order_details().keys())[-1]
                    # TODO: BUG
                    order.set_count(product, count)
                self.send_additional_product_selection(message)

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            chat_id = str(call.message.chat.id)
            # user_tg_id = str(call.message.from_user.id)
            # print(f"chat_id: {chat_id}")
            # print(f"user_tg_id: {user_tg_id}")
            if call.data == "finish_order":
                # Finish the order and notify the admin
                self.notify_admin(chat_id)
                self.bot.send_message(chat_id,
                                      "Дуже дякую за ваше замовлення, з вами дуже скоро зв'яжеться адмін для уточнень данних та відправки вам вашого замовлення")
                markup = types.InlineKeyboardMarkup()
                item_new_order = types.InlineKeyboardButton("Нове замовлення", callback_data="new_order")
                markup.add(item_new_order)
                self.bot.send_message(chat_id, "If you want to make a new order, click below:", reply_markup=markup)
            else:
                # Handle product selection and additional product selection
                product_slug = call.data.replace("_additional", "")
                product = Product(product_slug, Database(self.database_filename))
                if product:
                    order = Order(chat_id, Database(self.database_filename))
                    if "_additional" in call.data:
                        order.add_product(product.slug)
                        print(f"added product {product.slug}")
                        self.bot.send_message(chat_id,
                                              f"You chose {product.name}. How many packs of {product.name} would you like to buy? Please, write a number.")
                    else:
                        order.add_product(product.slug)
                        print(f"updated product {product.slug}")
                        self.bot.send_message(chat_id,
                                              f"You chose {product.name}. How many packs of {product.name} would you like to buy? Please, write a number.")

    def send_product_selection(self, message):
        markup = types.InlineKeyboardMarkup(row_width=2)
        products = Product.get_all_products(Database(self.database_filename))
        for product in products:
            item = types.InlineKeyboardButton(product.name, callback_data=product.slug)
            markup.add(item)
        self.bot.send_message(message.chat.id, "Choose a product:", reply_markup=markup)

        # Create an empty order for the user
        order = Order(str(message.from_user.id), Database(self.database_filename))
        # Database(self.database_filename).create_order(order)
        self.current_orders[str(message.from_user.id)] = order

    def send_additional_product_selection(self, message):
        markup = types.InlineKeyboardMarkup(row_width=2)
        products = Product.get_all_products(Database(self.database_filename))
        for product in products:
            item = types.InlineKeyboardButton("Так, хочу " + product.name, callback_data=product.slug + "_additional")
            markup.add(item)
        item_finish = types.InlineKeyboardButton("Ні, дякую, це все", callback_data="finish_order")
        markup.add(item_finish)
        self.bot.send_message(message.chat.id, "Do you want to order something else?", reply_markup=markup)

    def notify_admin(self, user_tg_id):
        order = self.current_orders.get(user_tg_id)
        if order:
            user = User(user_tg_id, Database(self.database_filename))
            # user = Database(self.database_filename).get_user(user_tg_id)
            if user:
                admin_message = f"New order from {user.name} (phone: {user.phone}):\n"
                for product, count in order.get_order_details().items():
                    admin_message += f"{product.name}: {count}\n"
                # TODO: Replace ADMIN_CHAT_ID with the actual chat ID of the admin
                self.bot.send_message(321107998, admin_message)

    def start_polling(self):
        self.bot.polling(none_stop=True)

