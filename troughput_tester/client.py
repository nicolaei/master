"""Simple roundtrip troughput using UDP

In this client we're trying to measure as often as possible to keep the link saturated.
This should hopfully give accurate results.
"""
import csv
import logging
import re
import selectors
import sys
import socket
import time
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

try:
    HOST = sys.argv[1]
except IndexError:
    HOST = "192.168.4.1"  # This is the IP access points are configured with by default.

PORT = 50000

BUFFER_SIZE = 2 ** 13
TIMEOUT = 0.25

BUFFER = {}
"""Holds packets that have been sent, but not recieved"""


def write(file_name: str, data: tuple):
    with open(file_name, "a") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([*data])


def db_reading():
    """Reads how strong the connection is in dB"""
    with open("/proc/net/wireless") as f:
        return float(f.readlines()[2].split()[3])


def create_data(order_number: int):
    """Creates a message consisting of the order number and padding"""
    order_num_characters = len(str(order_number))
    return f"{order_number}{'X' * (BUFFER_SIZE - order_num_characters)}".encode()


def parse_data(data: bytes):
    """Gets the order number in the given data"""
    return int(re.findall(r"\d+", data.decode())[0])


def send_packet(sock: socket.socket, order_number: int, recipient: tuple):
    """Sends a packet over the network and places it in the buffer"""
    data = create_data(order_number)

    BUFFER[order_number] = datetime.now()
    sock.sendto(data, recipient)


def recv_packet(sock: socket.socket):
    """Sends a packet over the network and places it in the buffer"""
    data = sock.recv(BUFFER_SIZE)

    after = datetime.now()

    order_number = parse_data(data)
    before = BUFFER.pop(order_number)

    return len(data), before.timestamp(), after.timestamp()


def client():
    poller = selectors.DefaultSelector()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(False)

    poller.register(sock, selectors.EVENT_READ | selectors.EVENT_WRITE)

    order_number = 0
    last_sent = datetime.now()
    while True:
        for key, mask in poller.select(timeout=0.1):
            try:
                if mask & selectors.EVENT_READ:
                    data = recv_packet(key.fileobj)
                    signal_strength = db_reading()
                    write("client_measurements.csv", (*data, signal_strength))

                # When the socket is ready to send
                elif mask & selectors.EVENT_WRITE:
                    if last_sent > datetime.now() - timedelta(milliseconds=100):
                        continue
                    send_packet(sock, order_number, (HOST, PORT))
                    order_number += 1
                    last_sent = datetime.now()
            except OSError as e:
                logger.warning(
                    f"{e.strerror}\nThis ususally happens while initially starting up."
                    f"Sleeping for 5 seconds before trying again."
                )
                time.sleep(5)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s][%(name)s][%(levelname)s]: %(message)s"
    )
    client()
