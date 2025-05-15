import sqlite3

def get_low_stock(threshold=5):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE quantity < ?", (threshold,))
    result = cursor.fetchall()
    conn.close()
    return result

def get_sales_summary():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("SELECT product_id, SUM(quantity), SUM(total_price) FROM sales GROUP BY product_id")
    rows = cursor.fetchall()
    conn.close()

    summary = []
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    for row in rows:
        product_id, qty, total = row
        cursor.execute("SELECT name FROM products WHERE id=?", (product_id,))
        product = cursor.fetchone()
        name = product[0] if product else "Unknown Product (ID: {})".format(product_id)
        summary.append((name, qty, total))
    conn.close()
    return summary

