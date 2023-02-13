import os
import http.server
import socketserver
import base64
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import logging
import time

PORT = 8000

# Define a custom handler that prompts for a password


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
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
        elif self.headers.get("Authorization") == "Basic " + base64.b64encode(f"{username}:{password}".encode()).decode():
            # Log the file being downloaded and the time it was downloaded
            logging.info(
                f"{self.path} downloaded at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            http.server.SimpleHTTPRequestHandler.do_GET(self)
        else:
            self.do_AUTHHEAD()
            self.wfile.write(b'not authenticated')


# Define the handler to be used
handler = CustomHTTPRequestHandler


def start_server(directory, username, password):
    # Change the current working directory to the specified directory
    os.chdir(directory)

    # Define the address to bind to
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print("Serving at URL http://localhost:" + str(PORT))
        messagebox.showinfo("Serving at", "URL: http://localhost:" + str(PORT))
        httpd.serve_forever()


# Create the GUI
root = tk.Tk()
root.title("HTTP Server")

frame = tk.Frame(root)
frame.pack()


def start_stop_server():
    global start_button, server_running
    if server_running:
        start_button.config(text="Start Server")
        server_running = False
    else:
        directory = filedialog.askdirectory(
            initialdir="/", title="Select the directory to share")
        if not directory:
            return
        username = tk.simpledialog.askstring(
            "Username", "Enter the username:", parent=root)
        if not username:
            return
        password = tk.simpledialog.askstring(
            "Password", "Enter the password:", show="*", parent=root)
        if not password:
            return
        start_button.config(text="Stop Server")
        server_running = True
        try:
            start_server(directory, username, password)
        except Exception as e:
            logging.error(e, exc_info=True)
            root.quit()


start_button = tk.Button(frame, text="Start Server", command=start_stop_server)
start_button.pack()

quit_button = tk.Button(frame, text="Quit", command=root.quit)
quit_button.pack()


server_running = False

root.mainloop()
