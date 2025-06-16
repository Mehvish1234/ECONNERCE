import http.server
import socketserver
import sys
import socket
import json
import urllib.request
import urllib.error
from urllib.parse import urlparse, parse_qs

PORT = 3000
AUTH_SERVER_PORT = 8080
CART_SERVER_PORT = 8081
DIRECTORY = "."

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        if self.path == '/dashboard.html':
            self.path = '/dashboard.html'
        elif self.path.startswith('/profile'):
            self.handle_profile_request()
            return
        elif self.path.startswith('/get_cart'):
            self.handle_cart_request()
            return
        return super().do_GET()

    def handle_profile_request(self):
        try:
            # Parse query parameters
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            user_id = query_params.get('user_id', [None])[0]

            if not user_id:
                self.send_error(400, 'User ID is required')
                return

            # Forward request to auth server
            auth_url = f'http://localhost:{AUTH_SERVER_PORT}/profile?user_id={user_id}'
            req = urllib.request.Request(auth_url)
            
            try:
                with urllib.request.urlopen(req) as response:
                    response_data = response.read()
                    self.send_response(response.status)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(response_data)
            except urllib.error.HTTPError as e:
                self.send_response(e.code)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(e.read())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def handle_cart_request(self):
        try:
            # Forward request to cart server
            cart_url = f'http://localhost:{CART_SERVER_PORT}{self.path}'
            req = urllib.request.Request(cart_url)
            
            try:
                with urllib.request.urlopen(req) as response:
                    response_data = response.read()
                    self.send_response(response.status)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(response_data)
            except urllib.error.HTTPError as e:
                self.send_response(e.code)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(e.read())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            # Determine which server to forward to based on the path
            if self.path in ['/login', '/signup']:
                server_url = f'http://localhost:{AUTH_SERVER_PORT}{self.path}'
            elif self.path in ['/add_to_cart', '/update_cart', '/remove_from_cart', '/clear_cart']:
                server_url = f'http://localhost:{CART_SERVER_PORT}{self.path}'
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Not found'}).encode())
                return
            
            headers = {
                'Content-Type': 'application/json',
                'Content-Length': str(len(post_data))
            }
            
            req = urllib.request.Request(server_url, data=post_data, headers=headers, method='POST')
            
            try:
                with urllib.request.urlopen(req) as response:
                    response_data = response.read()
                    self.send_response(response.status)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(response_data)
            except urllib.error.HTTPError as e:
                self.send_response(e.code)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(e.read())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

def start_server(port):
    try:
        with socketserver.TCPServer(("", port), Handler) as httpd:
            print(f"Server started successfully!")
            print(f"Open your browser and navigate to: http://localhost:{port}")
            print("Available pages:")
            print(f"- Home: http://localhost:{port}/index.html")
            print(f"- Shop: http://localhost:{port}/shop.html")
            print(f"- Login: http://localhost:{port}/login.html")
            print(f"- Signup: http://localhost:{port}/signup.html")
            print(f"- Profile: http://localhost:{port}/profile.html")
            print(f"- Dashboard: http://localhost:{port}/dashboard.html")
            print("\nPress Ctrl+C to stop the server...")
            httpd.serve_forever()
    except socket.error as e:
        if e.errno == 10048:  # Port already in use
            print(f"Error: Port {port} is already in use.")
            print("Please try a different port or close the application using this port.")
            sys.exit(1)
        else:
            print(f"Socket error: {e}")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    start_server(PORT) 