import http.server
import socketserver
import json
import sqlite3
from urllib.parse import parse_qs, urlparse
import os

PORT = 8081
DATABASE = 'ecom.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

class CartHandler(http.server.BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_GET(self):
        if self.path == '/get_cart':
            self.handle_get_cart()
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())

    def do_POST(self):
        if self.path == '/add_to_cart':
            self.handle_add_to_cart()
        elif self.path == '/update_cart':
            self.handle_update_cart()
        elif self.path == '/remove_from_cart':
            self.handle_remove_from_cart()
        elif self.path == '/clear_cart':
            self.handle_clear_cart()
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())

    def handle_get_cart(self):
        try:
            # Get user_id from query parameters
            query = parse_qs(urlparse(self.path).query)
            user_id = query.get('user_id', [None])[0]
            # Accept user_id from body if present (for future-proofing)
            if not user_id and self.command == 'POST':
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length > 0:
                    post_data = self.rfile.read(content_length)
                    data = json.loads(post_data.decode('utf-8'))
                    user_id = data.get('user_id')

            if not user_id:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'User ID is required'}).encode())
                return

            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Get cart items with product details
            cursor.execute('''
                SELECT ci.cart_item_id, ci.product_id, ci.quantity, p.name, p.price, p.image_url
                FROM cart_items ci
                JOIN products p ON ci.product_id = p.id
                WHERE ci.user_id = ?
                ORDER BY ci.added_at DESC
            ''', (user_id,))
            
            items = []
            for row in cursor.fetchall():
                items.append({
                    'id': row['product_id'],
                    'name': row['name'],
                    'price': row['price'],
                    'quantity': row['quantity'],
                    'image_url': row['image_url']
                })
            
            conn.close()
            
            self._set_headers()
            self.wfile.write(json.dumps({'items': items}).encode())
            
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def handle_add_to_cart(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Get user_id from body or query parameters
            query = parse_qs(urlparse(self.path).query)
            user_id = data.get('user_id') or query.get('user_id', [None])[0]

            if not user_id:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'User ID is required'}).encode())
                return

            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if item already exists in cart
            cursor.execute('''
                SELECT quantity FROM cart_items 
                WHERE user_id = ? AND product_id = ?
            ''', (user_id, data['id']))
            
            existing_item = cursor.fetchone()
            
            if existing_item:
                # Update quantity
                new_quantity = existing_item['quantity'] + data.get('quantity', 1)
                cursor.execute('''
                    UPDATE cart_items 
                    SET quantity = ?, added_at = CURRENT_TIMESTAMP 
                    WHERE user_id = ? AND product_id = ?
                ''', (new_quantity, user_id, data['id']))
            else:
                # Add new item
                cursor.execute('''
                    INSERT INTO cart_items (user_id, product_id, quantity)
                    VALUES (?, ?, ?)
                ''', (user_id, data['id'], data.get('quantity', 1)))
            
            conn.commit()
            
            # Get updated cart items
            cursor.execute('''
                SELECT ci.cart_item_id, ci.product_id, ci.quantity, p.name, p.price, p.image_url
                FROM cart_items ci
                JOIN products p ON ci.product_id = p.id
                WHERE ci.user_id = ?
                ORDER BY ci.added_at DESC
            ''', (user_id,))
            
            items = []
            for row in cursor.fetchall():
                items.append({
                    'id': row['product_id'],
                    'name': row['name'],
                    'price': row['price'],
                    'quantity': row['quantity'],
                    'image_url': row['image_url']
                })
            
            conn.close()
            
            self._set_headers()
            self.wfile.write(json.dumps({'items': items}).encode())
            
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def handle_update_cart(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Get user_id from body or query parameters
            query = parse_qs(urlparse(self.path).query)
            user_id = data.get('user_id') or query.get('user_id', [None])[0]

            if not user_id:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'User ID is required'}).encode())
                return

            conn = get_db_connection()
            cursor = conn.cursor()
            
            if data['quantity'] <= 0:
                # Remove item if quantity is 0 or negative
                cursor.execute('''
                    DELETE FROM cart_items 
                    WHERE user_id = ? AND product_id = ?
                ''', (user_id, data['productId']))
            else:
                # Update quantity
                cursor.execute('''
                    UPDATE cart_items 
                    SET quantity = ?, added_at = CURRENT_TIMESTAMP 
                    WHERE user_id = ? AND product_id = ?
                ''', (data['quantity'], user_id, data['productId']))
            
            conn.commit()
            
            # Get updated cart items
            cursor.execute('''
                SELECT ci.cart_item_id, ci.product_id, ci.quantity, p.name, p.price, p.image_url
                FROM cart_items ci
                JOIN products p ON ci.product_id = p.id
                WHERE ci.user_id = ?
                ORDER BY ci.added_at DESC
            ''', (user_id,))
            
            items = []
            for row in cursor.fetchall():
                items.append({
                    'id': row['product_id'],
                    'name': row['name'],
                    'price': row['price'],
                    'quantity': row['quantity'],
                    'image_url': row['image_url']
                })
            
            conn.close()
            
            self._set_headers()
            self.wfile.write(json.dumps({'items': items}).encode())
            
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def handle_remove_from_cart(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Get user_id from body or query parameters
            query = parse_qs(urlparse(self.path).query)
            user_id = data.get('user_id') or query.get('user_id', [None])[0]

            if not user_id:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'User ID is required'}).encode())
                return

            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Remove item
            cursor.execute('''
                DELETE FROM cart_items 
                WHERE user_id = ? AND product_id = ?
            ''', (user_id, data['productId']))
            
            conn.commit()
            
            # Get updated cart items
            cursor.execute('''
                SELECT ci.cart_item_id, ci.product_id, ci.quantity, p.name, p.price, p.image_url
                FROM cart_items ci
                JOIN products p ON ci.product_id = p.id
                WHERE ci.user_id = ?
                ORDER BY ci.added_at DESC
            ''', (user_id,))
            
            items = []
            for row in cursor.fetchall():
                items.append({
                    'id': row['product_id'],
                    'name': row['name'],
                    'price': row['price'],
                    'quantity': row['quantity'],
                    'image_url': row['image_url']
                })
            
            conn.close()
            
            self._set_headers()
            self.wfile.write(json.dumps({'items': items}).encode())
            
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def handle_clear_cart(self):
        try:
            # Get user_id from body or query parameters
            user_id = None
            if self.command == 'POST':
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length > 0:
                    post_data = self.rfile.read(content_length)
                    data = json.loads(post_data.decode('utf-8'))
                    user_id = data.get('user_id')
            if not user_id:
                query = parse_qs(urlparse(self.path).query)
                user_id = query.get('user_id', [None])[0]
            if not user_id:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'User ID is required'}).encode())
                return

            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Clear all items for user
            cursor.execute('DELETE FROM cart_items WHERE user_id = ?', (user_id,))
            conn.commit()
            conn.close()
            
            self._set_headers()
            self.wfile.write(json.dumps({'items': []}).encode())
            
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())

def run_server():
    with socketserver.TCPServer(("", PORT), CartHandler) as httpd:
        print(f"Cart server started on port {PORT}")
        print("Available endpoints:")
        print(f"- http://localhost:{PORT}/add_to_cart (POST)")
        print(f"- http://localhost:{PORT}/update_cart (POST)")
        print(f"- http://localhost:{PORT}/remove_from_cart (POST)")
        print(f"- http://localhost:{PORT}/get_cart (GET)")
        print("Press Ctrl+C to stop the server...")
        httpd.serve_forever()

if __name__ == '__main__':
    run_server() 