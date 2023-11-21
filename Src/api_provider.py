from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

import ssl

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
	# Parse the URL to extract parameters
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        # get the operation
        operation = query_params.get('operation', [''])[0]
        message = "Operation {}".format(operation)

	# send back the status
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(message, "utf8"))
        return

# Set the host and port for the server
host = '127.0.0.1' # bind all address 0.0.0.0
port = 443 # testing 2546

# Specify the path to your SSL certificate and private key files
ssl_certfile = 'khtcertificate.pem'
ssl_keyfile = 'khtprivate.pem'

# Create the server instance with the specified host, port, and SSL context
server = HTTPServer((host, port), MyHandler)
# server.socket = ssl.wrap_socket(server.socket, certfile=ssl_certfile, keyfile=ssl_keyfile, server_side=True)

print(f"Server started on http://{host}:{port}")

# Run the server
server.serve_forever()
