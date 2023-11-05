import sqlite3
def create_db():
    conn = sqlite3.connect('./test_bot_dobromir.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_id TEXT,
            name TEXT,
            phone TEXT,
            username TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            order_details TEXT,
            datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT,
            name TEXT
        )
    ''')

    # users = [
    #     ('123123123', 'Богдан', '+380123456789', 'bohdanUA'),
    #     ('456456456', 'Микита', '+380987654321', 'romashka'),
    #     ('789789789', 'Ірина', '+380111223344', 'IrenKrop')
    # ]
    # # Вставка даних до таблиці users
    # cursor.executemany('INSERT INTO users (tg_id, name, phone, username) VALUES (?, ?, ?, ?)', users)
    soups = [
        ('borsch', 'Борщ'),
        ('pea_soup', 'Гороховий суп'),
        ('vermicelli_soup', 'Вермішелевий суп')
    ]

    # Вставка даних до таблиці users
    cursor.executemany('INSERT INTO products (slug, name) VALUES (?, ?)', soups)

    conn.commit()
    conn.close()
