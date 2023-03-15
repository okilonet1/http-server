import os
import http.server
import socketserver
import logging
import socket
import threading

PORT = 8000

# Define the handler to be used
handler = http.server.SimpleHTTPRequestHandler


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

        # Start the server in a separate thread
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        # Wait for keyboard interrupt to stop the server
        try:
            while True:
                pass
        except KeyboardInterrupt:
            httpd.shutdown()
            server_thread.join()


if __name__ == '__main__':
    directory = input('Enter directory to share: ')
    start_server(directory)
