import pytest
from classes.Database import Database
from classes.Order import Order
from classes.User import User
from createdb import create_db
import os

@pytest.fixture
def test_database():
    create_db()
    db = Database('./test_bot_dobromir.db')
    user = User('41414141', db, './test_bot_dobromir.db', 'John', '380123456789', 'john')
    yield db

    db.close()  # Закрываем соединение с базой данных
    os.remove('./test_bot_dobromir.db')  # Удаляем файл базы данных

def test_create_order(test_database):
    order = Order('41414141', test_database, './test_bot_dobromir.db')
    assert order is not None
    assert order.id == 1
    assert order.order_details == {}
    assert order.status == 'new'

def test_db_to_dict(test_database):
    user = User('37373737', test_database, './test_bot_dobromir.db', 'John Doe', '380123456789', 'johndoe')
    order = Order('37373737', test_database, './test_bot_dobromir.db')
    print(user.id)
    order.add_product('borsch')
    order.set_count('borsch', 20)
    order_dict = order.db_to_dict()
    assert isinstance(order_dict, dict)
    assert order_dict['id'] == 1
    assert order_dict['user_id'] == 1
    assert order_dict['order_details'] == {'borsch': 20}
    assert order_dict['status'] == 'new'

def test_get_order_details(test_database):
    order = Order('41414141', test_database, './test_bot_dobromir.db')
    order.add_product('borsch')
    order.set_count('borsch', 20)
    order_details = order.get_order_details()
    assert order_details is not None
    assert order_details == {'borsch': 20}

def test_update_product(test_database):
    order = Order('41414141', test_database, './test_bot_dobromir.db')
    order.add_product('borsch')
    order.set_count('borsch', 20)
    order.update_product('borsch', 35)
    order_details = order.get_order_details()
    assert order_details is not None
    assert order_details == {'borsch': 35}

def test_add_product(test_database):
    order = Order('41414141', test_database, './test_bot_dobromir.db')
    order.add_product('borsch')
    order_details = order.get_order_details()
    assert order_details is not None
    assert order_details == {'borsch': 0}

def test_set_count(test_database):
    order = Order('41414141', test_database, './test_bot_dobromir.db')
    order.add_product('borsch')
    order.set_count('borsch', 20)
    order_details = order.get_order_details()
    assert order_details is not None
    assert order_details == {'borsch': 20}

def test_delete_product(test_database):
    order = Order('41414141', test_database, './test_bot_dobromir.db')
    order.add_product('borsch')
    order.set_count('borsch', 20)
    order.delete_product('borsch')
    order_details = order.get_order_details()
    assert order_details is not None
    assert order_details == {}

def test_confirmed_order(test_database):
    order = Order('41414141', test_database, './test_bot_dobromir.db')
    order.confirmed_order()
    assert order.status == 'confirmed'