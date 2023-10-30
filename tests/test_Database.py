import time
import pytest
import json
import sqlite3
from classes.Database import Database
from createdb import create_db
import os


@pytest.fixture
def test_database():
    create_db()
    db = Database('./test_bot_dobromir.db')

    yield db
    # time.sleep(10)
    del db
    # os.remove('./test_bot_dobromir.db')


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

def test_update_user(test_database):
    test_database.create_user('3', 'Bob', '111111111', 'bob')
    test_database.update_user('3', new_name='Bob Smith')
    user = test_database.get_user('3')
    assert user is not None
    assert user[2] == 'Bob Smith'

def test_get_product(test_database):
    product = test_database.get_product('borsch')
    assert product is not None
    assert product[1] == 'borsch'
    assert product[2] == 'Борщ'

def test_create_order(test_database):
    order_details = {'borsch': 20}
    assert test_database.create_order(1, order_details)
    order = test_database.get_last_new_by_tg_id('123123123')
    assert order is not None
    assert order[0] == 1  # Check order ID
    assert order[1] == 1  # Check user ID
    assert order[2] == json.dumps(order_details)  # Check order details
    assert order[4] == 'new'  # Check order status

