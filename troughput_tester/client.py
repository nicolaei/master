"""Simple roundtrip troughput using UDP

In this client we're trying to measure as often as possible to keep the link saturated.
This should hopfully give accurate results.
"""
import csv
import logging
import sys
import socket
import time
from datetime import datetime

logger = logging.getLogger(__name__)

HOST = sys.argv[1]
PORT = 50000
BUFFER_SIZE = 2**13
TIMEOUT = 0.25  # 250 ms

DATA = b"X" * BUFFER_SIZE


def write(file_name: str, data: tuple):
    with open(file_name, "a") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            *data
        ])


def measure(sock: socket.socket, recipient: tuple):
    """Gets roundtrip troughput for a single message on a socket

    :param sock: The socket to send and recive from
    :param recipient: A pair of host and port
    :returns: Various info about the given mesurement:
                * The amount of bytes sent
                * The time when the request was sent
                * The time when the request was responded to
    """
    before = datetime.now()

    sock.sendto(DATA, recipient)
    sock.recv(BUFFER_SIZE)

    after = datetime.now()

    return len(DATA), before.timestamp(), after.timestamp()


def client():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(TIMEOUT)
        while True:
            try:
                data = measure(sock, (HOST, PORT))
            except socket.timeout as e:
                logger.warning(f"The request to {HOST}:{PORT} timed out")
                data = (len(DATA), -1.0, -1.0)

            write("client_measurements.csv", data)
            time.sleep(0.05)  # Seems to help the troughput?


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s][%(name)s][%(levelname)s]: %(message)s"
    )
    client()
