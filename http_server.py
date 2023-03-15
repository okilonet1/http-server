import os
import http.server
import socketserver
import logging
import socket
import base64
import time

PORT = 8000

# Define the handler to be used


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="Auth example"')
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        auth_header = self.headers.get("Authorization")
        if not auth_header:
            self.do_AUTHHEAD()
            self.wfile.write(b'no auth header received')
        else:
            auth_decoded = base64.b64decode(auth_header[6:]).decode()
            username, password = auth_decoded.split(":")
            if username == "admin" and password == "admin":
                # Log the file being downloaded and the time it was downloaded
                logging.info(
                    f"{self.path} downloaded at {time.strftime('%Y-%m-%d %H:%M:%S')} from {self.client_address[0]}")
                http.server.SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.do_AUTHHEAD()
                self.wfile.write(b'not authenticated')


def start_server(directory):
    # Change the current working directory to the specified directory
    os.chdir(directory)

    # Set up logging
    logging.basicConfig(filename="http-server.log", level=logging.INFO,
                        format="%(asctime)s %(levelname)s: %(message)s")

    # Define the address to bind to
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        # Get the IP address of the machine running the server
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()

        print("Serving at URL http://" + ip_address + ":" + str(PORT))
        logging.info("Serving at URL http://" + ip_address + ":" + str(PORT))
        httpd.serve_forever()


if __name__ == '__main__':
    directory = input('Enter directory to share: ')
    start_server(directory)
