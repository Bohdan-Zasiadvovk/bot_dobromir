import pytest
import json
from classes.Database import Database
from createdb import create_db
import os


@pytest.fixture
def test_database():
    create_db()
    db = Database('./test_bot_dobromir.db')

    yield db

    db.close()  # Закрываем соединение с базой данных
    os.remove('./test_bot_dobromir.db')  # Удаляем файл базы данных

def test_create_user(test_database):
    assert test_database.create_user('123123123', 'John Doe', '123456789', 'johndoe')
    user = test_database.get_user('123123123')
    assert user is not None
    assert user[2] == 'John Doe'
    assert user[3] == '123456789'
    assert user[4] == 'johndoe'

def test_get_user(test_database):
    test_database.create_user('2', 'Alice', '987654321', 'alice')
    user = test_database.get_user('2')
    assert user is not None
    assert user[2] == 'Alice'
    assert user[3] == '987654321'
    assert user[4] == 'alice'

def test_get_or_create_user_existing_user(test_database):
    test_database.create_user('1', 'John Doe', '123456789', 'johndoe')
    user = test_database.get_or_create_user('1', 'John Doe', '123456789', 'johndoe')
    assert user is not None
    assert user[2] == 'John Doe'
    assert user[3] == '123456789'
    assert user[4] == 'johndoe'

def test_get_or_create_user_new_user(test_database):
    user = test_database.get_or_create_user('2', 'Alice', '987654321', 'alice')
    assert user is not None
    assert user[2] == 'Alice'
    assert user[3] == '987654321'
    assert user[4] == 'alice'

def test_update_user(test_database):
    test_database.create_user('979797', 'Bob', '111111111', 'bob')
    test_database.update_user('979797', new_name='Bob Smith')
    user = test_database.get_user('979797')
    assert user is not None
    assert user[2] == 'Bob Smith'

def test_get_product(test_database):
    product = test_database.get_product('borsch')
    assert product is not None
    assert product[1] == 'borsch'
    assert product[2] == 'Борщ'

def test_get_product_list(test_database):
    product_list = test_database.get_product_list()
    assert product_list[0] == (1, 'borsch', 'Борщ')
    assert product_list[1] == (2, 'pea_soup', 'Гороховий суп')
    assert product_list[2] == (3, 'vermicelli_soup', 'Вермішелевий суп')

def test_create_order(test_database):
    test_create_user(test_database)
    order_details = {'borsch': 20}
    assert test_database.create_order(1, order_details)
    order = test_database.get_last_new_by_tg_id('123123123')
    assert order is not None
    assert order[0] == 1  # Check order ID
    assert order[1] == 1  # Check user ID
    assert order[2] == json.dumps(order_details)  # Check order details
    assert order[4] == 'new'  # Check order status

def test_get_last_new_by_tg_id(test_database):
    test_create_user(test_database)
    test_create_order(test_database)
    last_new_by_tg_id = test_database.get_last_new_by_tg_id('123123123')
    assert last_new_by_tg_id[4] == 'new'


def test_update_order(test_database):
    test_create_user(test_database)
    test_create_order(test_database)


    updated_order_details = {'borsch': 55}
    assert test_database.update_order('1', updated_order_details, 'new')

    updated_order = test_database.get_last_new_by_tg_id('123123123')
    assert updated_order is not None
    assert json.loads(updated_order[2]) == updated_order_details
    assert updated_order[4] == 'new'

def test_set_status_confirmed(test_database):
    test_create_user(test_database)
    test_create_order(test_database)
    assert test_database.set_status_confirmed(1) == True


def test_set_status_done(test_database):
    test_create_user(test_database)
    test_create_order(test_database)
    assert test_database.set_status_done(1) == True

def test_set_status_deleted(test_database):
    test_create_user(test_database)
    test_create_order(test_database)
    assert test_database.set_status_deleted(1) == True