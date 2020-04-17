import logging
import sys
import socket
from datetime import datetime

logger = logging.getLogger(__name__)

HOST = sys.argv[1]
PORT = 50000
BUFFER_SIZE = 4096

DATA = b"X" * BUFFER_SIZE


def send_and_measure(sock: socket.socket, recipient: tuple):
    """Gets roundtrip troughput for a single message on a socket

    :param sock: The socket to send and recive from
    :param recipient: A pair of host and port
    :returns: Various info about the given mesurement:
                * The amount of bytes sent
                * The amount of seconds the round trip took (latency)
                * The send time
                * The recieve time
    """
    before = datetime.now()

    sock.sendto(DATA, recipient)
    sock.recv(BUFFER_SIZE)

    after = datetime.now()

    round_trip_time = (after - before).total_seconds()
    troughput = BUFFER_SIZE / round_trip_time

    return troughput, round_trip_time, before, after


def client():
    # Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        while True:
            # TODO: This should be every 250 ms!
            # TODO: Async plz
            send_and_measure(sock, (HOST, PORT))


if __name__ == "__main__":
    client()
