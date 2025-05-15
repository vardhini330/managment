import sqlite3
from datetime import datetime

def add_product(name, quantity, price):
    if name and quantity >= 0 and price >= 0:
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)", (name, quantity, price))
        conn.commit()
        conn.close()

def update_product(product_id, quantity, price):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET quantity=?, price=? WHERE id=?", (quantity, price, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()

def get_all_products():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return products

def sell_product(product_id, qty):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    cursor.execute("SELECT quantity, price FROM products WHERE id=?", (product_id,))
    result = cursor.fetchone()

    if result and result[0] >= qty:
        new_qty = result[0] - qty
        total_price = result[1] * qty
        cursor.execute("UPDATE products SET quantity=? WHERE id=?", (new_qty, product_id))
        cursor.execute("INSERT INTO sales (product_id, quantity, total_price, sale_date) VALUES (?, ?, ?, ?)", 
                       (product_id, qty, total_price, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False
def clear_all_data():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products")
    cursor.execute("DELETE FROM sales")
    conn.commit()
    conn.close()


