import pytest
from classes.Database import Database
from classes.User import User
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
    user = User('37373737', test_database, './test_bot_dobromir.db',  'John Doe', '380123456789', 'johndoe')
    assert user is not None
    assert user.tg_id == "37373737"
    assert user.name == 'John Doe'
    assert user.phone == '380123456789'
    assert user.username == 'johndoe'

def test_db_to_dict(test_database):
    user = User('37373737', test_database, './test_bot_dobromir.db', 'John Doe', '380123456789', 'johndoe')
    # assert isinstance(user, dict)
    assert False

def test_user_update_user(test_database):
    user = User('37373737', test_database, './test_bot_dobromir.db', 'John Doe', '380123456789', 'johndoe')
    user.update_user("Jane", "jane_doe")
    assert user.name == "Jane"
    assert user.username == "jane_doe"
