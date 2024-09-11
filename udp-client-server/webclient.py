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
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Resolving the IP address of a host
ip_address = socket.gethostbyname(host_name)
print("Resolved IP Address: ", ip_address, "\n")
# Server address and port
server_address = (ip_address, port)

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
    sock.sendto(request_bytes[i : i + packet_size], server_address)

# Setting a timeout for receiving (e.g., 2 seconds)
sock.settimeout(2.0)

# Receiving the response
buffer_size = 4096
response = b""
try:
    while True:
        buffer, sender = sock.recvfrom(buffer_size)
        print(buffer, sender)
        if not buffer:
            break
        response += buffer
except socket.timeout:
    print("Timeout reached, closing socket.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    sock.close()

print("Response received: ", response.decode())
