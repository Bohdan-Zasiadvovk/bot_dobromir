import pytest
from classes.Database import Database
from classes.Product import Product
from createdb import create_db
import os

@pytest.fixture
def test_database():
    create_db()
    db = Database('./test_bot_dobromir.db')

    yield db

    db.close()  # Закрываем соединение с базой данных
    os.remove('./test_bot_dobromir.db')  # Удаляем файл базы данных

def test_db_to_dict(test_database):
    product = Product('borsch', test_database)
    product_dict = product.db_to_dict()
    assert isinstance(product_dict, dict)
    assert product_dict['id'] == 1
    assert product_dict['slug'] == 'borsch'
    assert product_dict['name'] == 'Борщ'

def test_get_all_products(test_database):
    products = Product.get_all_products(test_database)
    assert products is not None
    assert products[0].slug == 'borsch'
    assert products[0].name == 'Борщ'
    assert products[1].slug == 'pea_soup'
    assert products[1].name == 'Гороховий суп'
    assert products[2].slug == 'vermicelli_soup'
    assert products[2].name == 'Вермішелевий суп'