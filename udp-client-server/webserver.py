import argparse
import logging
import os
import socket

logging.basicConfig(format="%(name)s:%(levelname)s:%(message)s")
logging.basicConfig(level=logging.debug)
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
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Setting socket options
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Binding the socket to an address
sock.bind(("", port))

# Defining some constants
crlf = "\r\n"

# Accepting a connection
request = ""
buffer_size = 4096
while True:
    logger.debug("Waiiting for a connection ....")
    while True:
        data, sender = sock.recvfrom(buffer_size)
        request += data.decode()
        if request.endswith(crlf * 2):
            break
    logger.debug(f"Request received: {request}")

    # Parsing the request
    try:
        header = request.strip().split(crlf * 2)[0]
        header_lines = header.strip().split(crlf)
        request_type, path, protocol = header_lines[0].split()
        _, path = os.path.split(path)  # Stripping the path

        # Creating a generic response
        response = "Received data from the client"

    except Exception:
        response = ""
        logger.debug("An error occurred while processing the request.")

    # Sending the response
    sock.sendto(response.encode(), sender)
