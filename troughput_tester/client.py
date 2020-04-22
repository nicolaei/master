"""Simple roundtrip troughput using UDP

In this client we're trying to measure as often as possible to keep the link saturated.
This should hopfully give accurate results.
"""
import logging
import sys
import socket
from datetime import datetime

logger = logging.getLogger(__name__)

HOST = sys.argv[1]
PORT = 50000
BUFFER_SIZE = 4096
TIMEOUT = 0.25  # 250 ms

DATA = b"X" * BUFFER_SIZE


def measure(sock: socket.socket, recipient: tuple):
    """Gets roundtrip troughput for a single message on a socket

    :param sock: The socket to send and recive from
    :param recipient: A pair of host and port
    :returns: Various info about the given mesurement:
                * The amount of bytes sent
                * The amount of seconds the round trip took (latency)
                * The time when the request was sent
                * The time when the request was responded to
    """
    before = datetime.now()

    sock.sendto(DATA, recipient)
    sock.recv(BUFFER_SIZE)

    after = datetime.now()

    round_trip_time = (after - before).total_seconds()
    troughput = BUFFER_SIZE / round_trip_time

    return troughput, round_trip_time, before, after


def client():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(TIMEOUT)
        while True:
            measure(sock, (HOST, PORT))


if __name__ == "__main__":
    client()
