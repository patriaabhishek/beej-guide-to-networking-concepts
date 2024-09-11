import json
import select
import socket
from collections import deque

PACKET_SIZE_LEN = 2
BUFFER_SIZE = 4096
client_data = {}
message_q = deque()


def get_next_packet(sock, packet_buffer):
    while True:
        packet_buffer += sock.recv(BUFFER_SIZE)
        if len(packet_buffer) == 0:
            return None
        if len(packet_buffer) >= PACKET_SIZE_LEN:
            packet_size = int.from_bytes(packet_buffer[:PACKET_SIZE_LEN], "big")
        if len(packet_buffer) >= PACKET_SIZE_LEN + packet_size:
            packet = packet_buffer[: PACKET_SIZE_LEN + packet_size]
            packet_buffer = packet_buffer[PACKET_SIZE_LEN + packet_size :]
            return packet


def extract_data(packet):
    data = packet[PACKET_SIZE_LEN:]
    data = data.decode("utf-8")
    data = json.loads(data)
    return data


def event_action(conn, data, read_set):
    if data["type"] == "hello":
        """
        "type": "hello"
        "nick": "[user nickname]"
        """
        client_data[conn]["nick"] = data["nick"]

    if data["type"] == "chat":
        """
        "type": "chat"
        "message": "[message]"
        """
        message = data["message"]
        message_q.append(message)

    if data["type"] == "join":
        """
        "type": "join"
        "nick": "[joiner's nickname]"
        """
        message = f"*** {client_data[conn]["nick"]} has joined the chat ***"
        message_q.append(message)

    if data["type"] == "leave":
        """
        "type": "leave"
        "nick": "[leaver's nickname]"
        """
        message = f"*** {client_data[conn]["nick"]} has left the chat ***"
        message_q.append(message)
        client_data.pop(conn)
        read_set.remove(conn)


def run_server(port):
    listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listening_socket.bind(("", port))
    listening_socket.listen()
    logger.info(f"Server listening on port {port}")
    read_set, write_set, error_set = set([listening_socket]), set(), set()
    while True:
        read_sockets, write_sockets, error_sockets = select.select(
            read_set, write_set, error_set
        )

        for sock in read_sockets:
            if sock is listening_socket:
                conn, addr = listening_socket.accept()
                read_set.add(conn)
                client_data[conn] = {"addr": addr, "buffer": b"", "nick": None}

            else:
                data = sock
                if not data:
                    read_set.remove(sock)
                    sock.close()
                    logger.info(f"{addr}: disconnected")
                else:
                    get_next_packet()

                    client_data[sock]["buffer"] += data
                    logger.info(f"{addr} {len(data)} bytes: {data.decode()}")
