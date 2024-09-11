import argparse
import socket

# Parsing arguments for the browser
parser = argparse.ArgumentParser(description="Basic Socket Programming")
parser.add_argument("--host", help="Host name", default="example.com", required=False)
parser.add_argument("--port", help="Port number", default=80, required=False, type=int)
args = parser.parse_args()

# Parsing the arguments
host_name = args.host
port = args.port

# Creating a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Resolving the IP address of a host
ip_address = socket.gethostbyname(host_name)
print("Resolved IP Address: ", ip_address, "\n")

# Connecting to a host
sock.connect((ip_address, port))
crlf = "\r\n"

# Building a HTTP request
request = ""
request += f"GET / HTTP/1.1{crlf}"
request += f"Host: {host_name}{crlf}"
request += f"Connection: close{crlf}"
request += f"{crlf}"

# Encoding the request
request_bytes = request.encode()
packet_size = 1024

# Sending the request
for i in range(0, len(request_bytes), packet_size):
    sock.send(request_bytes[i : i + packet_size])

# Receiving the response
buffer_size = 4096
response = b""
while True:
    buffer = sock.recv(buffer_size)
    if not buffer:
        break
    response += buffer
print(response.decode())

# Closing the socket
sock.close()
