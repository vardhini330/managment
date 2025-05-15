import sqlite3

def init_db():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            quantity INTEGER,
            total_price REAL,
            sale_date TEXT,
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    ''')

    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ('admin', 'admin123'))
    conn.commit()
    conn.close()

