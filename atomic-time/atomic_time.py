import socket

# Creating a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Resolving the IP address of a host
ip_address = socket.gethostbyname("time.nist.gov")
print("Resolved IP Address: ", ip_address, "\n")
# Fixing port
port = 13

# Connecting to a host
sock.connect((ip_address, port))
# Receiving the response
buffer_size = 4096
response = b""
while True:
    buffer = sock.recv(buffer_size)
    if not buffer:
        break
    response += buffer
sock.close()
time = int.from_bytes(response, "big")
print(time)
