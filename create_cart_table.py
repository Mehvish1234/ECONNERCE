import sqlite3

def create_cart_table():
    # Create database connection
    conn = sqlite3.connect('ecom.db')
    cursor = conn.cursor()

    # Create cart_items table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cart_items (
        cart_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,
        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES products (id),
        UNIQUE(user_id, product_id)
    )
    ''')

    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("Cart items table created successfully!")

if __name__ == '__main__':
    create_cart_table() 