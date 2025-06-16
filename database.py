import sqlite3
import hashlib
import os

def init_db():
    # Create database connection
    conn = sqlite3.connect('ecom.db')
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create user_details table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_details (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        first_name TEXT,
        last_name TEXT,
        address TEXT,
        city TEXT,
        state TEXT,
        country TEXT,
        phone TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')

    # Create cart_items table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cart_items (
        cart_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,
        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        UNIQUE(user_id, product_id)
    )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, email, password, details=None):
    conn = sqlite3.connect('ecom.db')
    cursor = conn.cursor()
    
    try:
        # Insert user
        hashed_password = hash_password(password)
        cursor.execute('''
        INSERT INTO users (username, email, password)
        VALUES (?, ?, ?)
        ''', (username, email, hashed_password))
        
        user_id = cursor.lastrowid
        
        # Insert user details if provided
        if details:
            cursor.execute('''
            INSERT INTO user_details (
                user_id, first_name, last_name, address,
                city, state, country, phone
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id, details.get('first_name'), details.get('last_name'),
                details.get('address'), details.get('city'), details.get('state'),
                details.get('country'), details.get('phone')
            ))
        
        conn.commit()
        return True, user_id
    except sqlite3.IntegrityError as e:
        if "username" in str(e):
            return False, "Username already exists"
        elif "email" in str(e):
            return False, "Email already exists"
        return False, str(e)
    finally:
        conn.close()

def verify_user(username, password):
    conn = sqlite3.connect('ecom.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        SELECT id, password FROM users WHERE username = ?
        ''', (username,))
        
        result = cursor.fetchone()
        if result:
            user_id, stored_password = result
            if stored_password == hash_password(password):
                return True, user_id
        return False, "Invalid username or password"
    finally:
        conn.close()

def get_user_details(user_id):
    conn = sqlite3.connect('ecom.db')
    cursor = conn.cursor()
    
    try:
        # Get user data
        cursor.execute('''
        SELECT username, email FROM users WHERE id = ?
        ''', (user_id,))
        user_data = cursor.fetchone()
        
        if not user_data:
            return None
        
        # Get user details
        cursor.execute('''
        SELECT first_name, last_name, address, city, state, country, phone
        FROM user_details WHERE user_id = ?
        ''', (user_id,))
        details = cursor.fetchone()
        
        user_info = {
            'id': user_id,
            'username': user_data[0],
            'email': user_data[1],
            'details': {
                'first_name': details[0] if details else None,
                'last_name': details[1] if details else None,
                'address': details[2] if details else None,
                'city': details[3] if details else None,
                'state': details[4] if details else None,
                'country': details[5] if details else None,
                'phone': details[6] if details else None
            } if details else None
        }
        
        return user_info
    finally:
        conn.close()

def update_user_details(user_id, details):
    conn = sqlite3.connect('ecom.db')
    cursor = conn.cursor()
    
    try:
        # Check if user details exist
        cursor.execute('SELECT id FROM user_details WHERE user_id = ?', (user_id,))
        exists = cursor.fetchone()
        
        if exists:
            # Update existing details
            cursor.execute('''
            UPDATE user_details
            SET first_name = ?, last_name = ?, address = ?,
                city = ?, state = ?, country = ?, phone = ?
            WHERE user_id = ?
            ''', (
                details.get('first_name'), details.get('last_name'),
                details.get('address'), details.get('city'),
                details.get('state'), details.get('country'),
                details.get('phone'), user_id
            ))
        else:
            # Insert new details
            cursor.execute('''
            INSERT INTO user_details (
                user_id, first_name, last_name, address,
                city, state, country, phone
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id, details.get('first_name'), details.get('last_name'),
                details.get('address'), details.get('city'),
                details.get('state'), details.get('country'),
                details.get('phone')
            ))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating user details: {e}")
        return False
    finally:
        conn.close()

def add_to_cart(user_id, product_id, quantity=1):
    conn = sqlite3.connect('ecom.db')
    cursor = conn.cursor()
    try:
        # Check if item already exists in cart
        cursor.execute('SELECT quantity FROM cart_items WHERE user_id = ? AND product_id = ?', 
                 (user_id, product_id))
        existing_item = cursor.fetchone()
        
        if existing_item:
            # Update quantity if item exists
            new_quantity = existing_item[0] + quantity
            cursor.execute('''
                UPDATE cart_items 
                SET quantity = ?, added_at = CURRENT_TIMESTAMP 
                WHERE user_id = ? AND product_id = ?
            ''', (new_quantity, user_id, product_id))
        else:
            # Insert new item if it doesn't exist
            cursor.execute('''
                INSERT INTO cart_items (user_id, product_id, quantity)
                VALUES (?, ?, ?)
            ''', (user_id, product_id, quantity))
        
        conn.commit()
        return True, "Item added to cart successfully"
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

def get_cart_items(user_id):
    conn = sqlite3.connect('ecom.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT ci.*, p.name, p.price, p.image_url
            FROM cart_items ci
            JOIN products p ON ci.product_id = p.id
            WHERE ci.user_id = ?
            ORDER BY ci.added_at DESC
        ''', (user_id,))
        items = cursor.fetchall()
        return True, items
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def update_cart_item(user_id, product_id, quantity):
    conn = sqlite3.connect('ecom.db')
    cursor = conn.cursor()
    try:
        if quantity <= 0:
            # Remove item if quantity is 0 or negative
            cursor.execute('DELETE FROM cart_items WHERE user_id = ? AND product_id = ?',
                     (user_id, product_id))
        else:
            # Update quantity
            cursor.execute('''
                UPDATE cart_items 
                SET quantity = ?, added_at = CURRENT_TIMESTAMP 
                WHERE user_id = ? AND product_id = ?
            ''', (quantity, user_id, product_id))
        
        conn.commit()
        return True, "Cart updated successfully"
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

def remove_from_cart(user_id, product_id):
    conn = sqlite3.connect('ecom.db')
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM cart_items WHERE user_id = ? AND product_id = ?',
                 (user_id, product_id))
        conn.commit()
        return True, "Item removed from cart successfully"
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
    
    # Add a test user if it doesn't exist
    print("Checking for test user...")
    conn = sqlite3.connect('ecom.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = 'test_user'")
    user_exists = cursor.fetchone()
    conn.close()

    if not user_exists:
        print("Creating test user...")
        success, result = create_user(
            'test_user', 
            'test@example.com', 
            'password123',
            {
                'first_name': 'Test',
                'last_name': 'User',
                'address': '123 Test Street',
                'city': 'Testville',
                'state': 'TS',
                'country': 'Testland',
                'phone': '555-0123'
            }
        )
        if success:
            print("Test user 'test_user' created successfully with password 'password123'.")
        else:
            print(f"Failed to create test user: {result}")
    else:
        print("Test user 'test_user' already exists.") 