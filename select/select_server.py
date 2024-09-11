# Example usage:
#
# python select_server.py 3490

import logging
import select
import socket
import sys

logging.basicConfig(format="%(name)s:%(levelname)s:%(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)


def run_server(port):
    listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listening_socket.bind(("", port))
    listening_socket.listen()
    logger.info(f"Listening on port {port}")
    read_set, write_set, error_set = set([listening_socket]), set(), set()
    while True:
        logger.info("Waiting for connections...")
        read_socks, write_socks, error_socks = select.select(
            read_set, write_set, error_set
        )

        for sock in read_socks:
            if sock is listening_socket:
                conn, addr = listening_socket.accept()
                logger.info(f"{addr}: connected")
                read_set.add(conn)
            else:
                data = sock.recv(1024)
                addr = sock.getpeername()
                if not data:
                    read_set.remove(sock)
                    sock.close()
                    logger.info(f"{addr}: disconnected")
                else:
                    logger.info(f"{addr} {len(data)} bytes: {data.decode()}")


# --------------------------------#
# Do not modify below this line! #
# --------------------------------#


def usage():
    print("usage: select_server.py port", file=sys.stderr)


def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
