import sqlite3

def init_products():
    # Create database connection
    conn = sqlite3.connect('ecom.db')
    cursor = conn.cursor()

    # Create products table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        stock INTEGER NOT NULL,
        image_url TEXT,
        category TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Sample products data
    sample_products = [
        ('Wireless Headphones', 'High-quality wireless headphones with noise cancellation', 99.99, 50, 
         'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60', 'Electronics'),
        ('Smart Watch', 'Feature-rich smartwatch with health monitoring', 149.99, 30,
         'https://images.unsplash.com/photo-1523275335684-37898b6baf30?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60', 'Electronics'),
        ('Running Shoes', 'Comfortable running shoes for all terrains', 79.99, 100,
         'https://images.unsplash.com/photo-1542291026-7eec264c27ff?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60', 'Clothing'),
        ('Laptop Backpack', 'Durable laptop backpack with multiple compartments', 49.99, 75,
         'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60', 'Accessories'),
        ('Coffee Maker', 'Programmable coffee maker with thermal carafe', 89.99, 25,
         'https://images.unsplash.com/photo-1570087935864-1a67ddf02395?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60', 'Home & Kitchen'),
        ('Yoga Mat', 'Non-slip yoga mat with carrying strap', 29.99, 150,
         'https://images.unsplash.com/photo-1592432678016-e910b452f9a2?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60', 'Sports')
    ]

    # Insert sample products
    cursor.executemany('''
    INSERT OR IGNORE INTO products (name, description, price, stock, image_url, category)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', sample_products)

    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("Products table initialized and sample products added successfully!")

if __name__ == '__main__':
    init_products() 