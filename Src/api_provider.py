from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import ssl

import postgreSQL

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL to extract parameters
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        # get the operation
        operation = query_params.get('operation', [''])[0]
        geojson_data = ""
        marker1 = query_params.get('marker1', [''])[0]
        marker2 = query_params.get('marker2', [''])[0]
        message = "Operation {}".format(operation)

        if operation == "pull-static-data":
            geojson_data = postgreSQL.get_table("village_test")
        elif operation == "get-distance":
            message = "TODO Return distance between {} to {}".format(marker1, marker2)
        elif operation == "find-nearest-hospital":
            message = "TODO"

        # Enable CORS
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # You can replace '*' with specific origins
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Origin, Content-Type')

        self.end_headers()

        # Return the response and data
        try:
            self.wfile.write(bytes(geojson_data, "utf8"))
        except BrokenPipeError:
            pass  # Ignore BrokenPipeError

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
