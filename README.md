# HTTP Server with FTP Functionality

This program allows you to share files in a specified directory on your computer through a web browser, with FTP-like functionality. The files in the specified directory will be available for download by visiting a URL in a web browser.

## Requirements

- Python 3
- Tkinter

## Features

- Prompts for the directory to share
- Prompts for a username and password for authentication
- Logs all files downloaded with timestamps
- All logs are stored in a file called `ftp-server.logs`
- Displays the URL the site can be accessed from after the server starts
- Start button alternates between start and stop
- Error logging and quitting if an error occurs

## Usage

1. Clone or download the repository
2. Navigate to the project directory in the terminal or command prompt
3. Run the `http_server.py` file with `python3 http_server.py`
4. Follow the prompt to select the directory to share, enter a username and password, and start the server
5. Access the shared files by visiting the URL displayed in the prompt in a web browser

## Note

This program should not be used for production purposes and is for educational and demonstration purposes only.
