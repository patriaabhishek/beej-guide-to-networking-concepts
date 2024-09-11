import argparse
import logging
import os
import socket

logging.basicConfig(format="%(name)s:%(levelname)s:%(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Parsing arguments for the browser
parser = argparse.ArgumentParser(description="Basic Socket Programming")
parser.add_argument(
    "--port", help="Port number to listen to", default=28333, required=False, type=int
)
args = parser.parse_args()

port = args.port

# Creating a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Setting socket options
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Binding the socket to an address
sock.bind(("", port))

# Listening for incoming connections
sock.listen()

# Defining some constants
crlf = "\r\n"
mime_types = {
    ".txt": "text/plain",
    ".html": "text/html",
}

# Accepting a connection
buffer_size = 4096
while True:
    logger.debug(f"{'#'*50}")
    logger.debug("Listening for incoming connections...")
    logger.debug(f"{'#'*50}")
    conn, addr = sock.accept()
    logger.debug(f"Connected to {addr}")
    request = ""
    while True:
        data = conn.recv(buffer_size)
        request += data.decode()
        if request.endswith(crlf * 2):
            break
    logger.debug("Request received:\n")
    logger.debug(request)
    logger.debug("\n")

    # Parsing the request
    try:
        header = request.strip().split(crlf * 2)[0]
        header_lines = header.strip().split(crlf)
        request_type, path, protocol = header_lines[0].split()
        _, path = os.path.split(path)  # Stripping the path
        file_name, file_type = os.path.splitext(path)
        logger.debug(f"File details: {file_name}{file_type}")
        mime_type = mime_types[file_type]

        # Reading the file and building the response
        try:
            with open(path, "rb") as file:
                content = file.read()
            content_length = len(content)
            response = ""
            response += f"HTTP/1.1 200 OK{crlf}"
            response += f"Content-Type: {mime_type}{crlf}"
            response += f"Content-Length: {content_length}{crlf}"
            response += f"Connection: close{crlf}{crlf}"
            response += f"{content.decode()}{crlf}"

        except FileNotFoundError:
            content = "404 Not Found"
            response = ""
            response += f"HTTP/1.1 404 Not Found{crlf}"
            response += f"Content-Type: text/plain{crlf}"
            response += f"Content-Length: 13{crlf}"
            response += f"Connection: close{crlf}{crlf}"
            response += f"{content}{crlf}"
    except Exception:
        response = ""
        logger.debug("An error occurred while processing the request.")
    # Sending the response
    conn.send(response.encode())

    # Closing the connection
    conn.close()
    logging.debug(f"{'#'*50}")
