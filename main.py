from classes.Order import Order
from classes.Database import Database
import sqlite3


if __name__ == "__main__":
    tg_id = "123123123"
    #d = dict()
    db_cursor = Database()
    #print(db_cursor.create_order(1, d))
    NOrder = Order(tg_id, db_cursor)
    #print(NOrder.user)



    print(NOrder.get_order_details())
#     # Тест 2: Оновлення продукту у замовленні
#     print("Test 2: Updating a product in the order")
#     product_slug = "borsch"
#     new_count = 5
#     NOrder.update_product(product_slug, new_count)
#     print("Updated order details:", NOrder.get_order_details())
#     # Тест 3: Додавання нового продукту до замовлення
#     print("Test 3: Adding a new product to the order")
#     new_product_slug = "pea_soup"
#     NOrder.add_product(new_product_slug)
#     print("Updated order details:", NOrder.get_order_details())
#     # Тест 4: Видалення продукту з замовлення
#     print("Test 4: Deleting a product from the order")
#     NOrder.delete_product(product_slug)
#     print("Updated order details:", NOrder.get_order_details())
#     # Тест 5: Підтвердження замовлення
#     print("Test 5: Confirming the order")
#     NOrder.confirmed_order()
#     print("Order status:", NOrder.status)

#     conn = sqlite3.connect('test_bot_dobromir.db')
#     cursor = conn.cursor()
#     cursor.execute('DELETE FROM orders')
#     conn.commit()
#     conn.close()
