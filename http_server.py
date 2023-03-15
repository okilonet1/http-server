import os
import http.server
import socketserver
import logging
import socket
import configparser
import base64

PORT = 8000

# Get the directory of the Python file
dir_path = os.path.dirname(os.path.realpath(__file__))

# Read the usernames and passwords from the config file
# config = configparser.ConfigParser()
# config.read(os.path.join(dir_path, 'server.config'))
# users = dict(config['users'])
# print(users)
users = {}

with open('server.config', 'r') as f:
    for line in f:
        line = line.strip()
        if line:
            username, password = line.split(':')
            users[username] = password

print(users)

# Define the handler to be used


class AuthHandler(http.server.SimpleHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="Auth example"')
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        if self.headers.get("Authorization") is None:
            self.do_AUTHHEAD()
            self.wfile.write(b'no auth header received')
        else:
            auth = self.headers.get("Authorization").split()[1]
            auth = base64.b64decode(auth).decode()
            username, password = auth.split(":")
            if username in users and users[username] == password:
                # Log the file being downloaded and the time it was downloaded
                logging.info(
                    f"{self.path} accessed by {self.client_address[0]} at {self.log_date_time_string()}")
                http.server.SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.do_AUTHHEAD()
                self.wfile.write(b'not authenticated')


# Define the handler to be used
handler = AuthHandler


def start_server(directory):
    # Change the current working directory to the specified directory
    os.chdir(directory)

    # Define the address to bind to
    with socketserver.TCPServer(("", PORT), handler) as httpd:
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
