import http.server
import ssl

# Define the server's request handler
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/cleaned_entities.json':  # The path to the JSON file
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            with open('cleaned_entities.json', 'r') as file:  # The actual JSON file on your system
                self.wfile.write(file.read().encode())
        else:
            self.send_error(404)

# Set up the server with the handler and port number
httpd = http.server.HTTPServer(('localhost', 4443), MyHandler)

# Create an SSL context for the HTTPS connection
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile='server.crt', keyfile='server.key')
    
# Wrap the server's socket with SSL
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print("Serving on https://localhost:4443")
httpd.serve_forever()
