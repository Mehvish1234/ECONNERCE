from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
from database import create_user, verify_user, get_user_details, update_user_details
import os

class AuthHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200, content_type='application/json'):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def _send_json_response(self, data, status_code=200):
        self._set_headers(status_code)
        self.wfile.write(json.dumps(data).encode())

    def do_OPTIONS(self):
        self._set_headers()

    def do_GET(self):
        if self.path.startswith('/static/'):
            # Serve static files
            file_path = self.path[1:]  # Remove leading slash
            try:
                with open(file_path, 'rb') as f:
                    content_type = 'text/css' if file_path.endswith('.css') else 'application/javascript'
                    self._set_headers(content_type=content_type)
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self._send_json_response({'error': 'File not found'}, 404)
        elif self.path.endswith('.html'):
            # Serve HTML files
            file_path = self.path[1:]  # Remove leading slash
            try:
                with open(file_path, 'rb') as f:
                    self._set_headers(content_type='text/html')
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self._send_json_response({'error': 'File not found'}, 404)
        elif self.path.startswith('/profile'):
            # Handle profile request
            try:
                # Parse query parameters
                parsed_url = urllib.parse.urlparse(self.path)
                query_params = urllib.parse.parse_qs(parsed_url.query)
                user_id = query_params.get('user_id', [None])[0]

                if not user_id:
                    self._send_json_response({'error': 'User ID is required'}, 400)
                    return

                user_info = get_user_details(user_id)
                if not user_info:
                    self._send_json_response({'error': 'User not found'}, 404)
                    return

                self._send_json_response(user_info)
            except Exception as e:
                self._send_json_response({'error': str(e)}, 500)
        else:
            self._send_json_response({'error': 'Not found'}, 404)

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data)
            except json.JSONDecodeError:
                self._send_json_response({'error': 'Invalid JSON data'}, 400)
                return

            if self.path == '/signup':
                # Validate required fields
                required_fields = ['username', 'email', 'password']
                missing_fields = [field for field in required_fields if not data.get(field)]
                if missing_fields:
                    self._send_json_response({'error': f'Missing required fields: {", ".join(missing_fields)}'}, 400)
                    return

                success, result = create_user(
                    data.get('username'),
                    data.get('email'),
                    data.get('password'),
                    {
                        'first_name': data.get('first_name'),
                        'last_name': data.get('last_name'),
                        'address': data.get('address'),
                        'city': data.get('city'),
                        'state': data.get('state'),
                        'country': data.get('country'),
                        'phone': data.get('phone')
                    }
                )
                
                if success:
                    self._send_json_response({'message': 'User created successfully', 'user_id': result})
                else:
                    self._send_json_response({'error': result}, 400)

            elif self.path == '/login':
                # Validate required fields
                if not data.get('username') or not data.get('password'):
                    self._send_json_response({'error': 'Username and password are required'}, 400)
                    return

                success, result = verify_user(data.get('username'), data.get('password'))
                
                if success:
                    user_info = get_user_details(result)
                    self._send_json_response({
                        'message': 'Login successful',
                        'user_id': result,
                        'user_info': user_info
                    })
                else:
                    self._send_json_response({'error': result}, 401)

            else:
                self._send_json_response({'error': 'Not found'}, 404)
        except Exception as e:
            self._send_json_response({'error': f'Server error: {str(e)}'}, 500)

    def do_PUT(self):
        if self.path == '/profile':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            user_id = data.get('user_id')
            if not user_id:
                self._send_json_response({'error': 'User ID required'}, 400)
                return
            
            success = update_user_details(user_id, {
                'first_name': data.get('first_name'),
                'last_name': data.get('last_name'),
                'address': data.get('address'),
                'city': data.get('city'),
                'state': data.get('state'),
                'country': data.get('country'),
                'phone': data.get('phone')
            })
            
            if success:
                self._send_json_response({'message': 'Profile updated successfully'})
            else:
                self._send_json_response({'error': 'Failed to update profile'}, 500)
        else:
            self._send_json_response({'error': 'Not found'}, 404)

def run_server(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, AuthHandler)
    print(f"Server started on port {port}")
    print("\nAvailable endpoints:")
    print(f"- http://localhost:{port}/signup (POST)")
    print(f"- http://localhost:{port}/login (POST)")
    print(f"- http://localhost:{port}/profile (PUT)")
    print("\nStatic files:")
    print(f"- http://localhost:{port}/index.html")
    print(f"- http://localhost:{port}/shop.html")
    print(f"- http://localhost:{port}/login.html")
    print(f"- http://localhost:{port}/signup.html")
    print(f"- http://localhost:{port}/profile.html")
    print("\nPress Ctrl+C to stop the server...")
    httpd.serve_forever()

if __name__ == '__main__':
    # Initialize the database
    from database import init_db
    init_db()
    
    # Run the server
    run_server() 