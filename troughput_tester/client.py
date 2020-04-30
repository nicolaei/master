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

try:
    HOST = sys.argv[1]
except IndexError:
    HOST = "192.168.4.1"  # This is the IP access points are configured with by default.

PORT = 50000
BUFFER_SIZE = 2**13
TIMEOUT = 0.25  # 250 ms

DATA = b"X" * BUFFER_SIZE


def write(file_name: str, data: tuple):
    with open(file_name, "a") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([*data])


def db_reading():
    """Reads how strong the connection is in dB"""
    with open("/proc/net/wireless") as f:
        return float(f.readlines()[2].split()[3])


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
                time.sleep(5)
                continue
            except OSError as e:
                logger.warning(
                    f"Network could not be reached! This typically happens at boot. "
                    f"This warning should stop appearing in a few seconds. "
                    f"Waiting 5 seconds."
                )
                time.sleep(5)
                continue

            try:
                signal_strength = db_reading()
            except IndexError:
                logger.warning(
                    "Measurement Error: Couldn't read dB or latency.\n"
                    "You're probably not connected to a network. This mostly "
                    "happens if you just booted your device."
                )
                signal_strength = None

            write("client_2_measurements.csv", (*data, signal_strength))
            time.sleep(0.05)  # Seems to help the troughput?


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s][%(name)s][%(levelname)s]: %(message)s"
    )
    client()
