import logging
import selectors
import socket

logger = logging.getLogger(__name__)

HOST = "0.0.0.0"
PORT = 50000
BUFFER_SIZE = 2 ** 13


def server():
    poller = selectors.DefaultSelector()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    sock.setblocking(False)

    poller.register(sock, selectors.EVENT_READ)

    while True:
        for key, mask in poller.select(timeout=0.1):
            if mask & selectors.EVENT_READ:
                data, address = key.fileobj.recvfrom(BUFFER_SIZE)
                key.fileobj.sendto(data, address)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s][%(name)s][%(levelname)s]: %(message)s"
    )

    logger.info("Starting troughput server")
    server()
