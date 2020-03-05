#!/usr/bin/env python3
"""Continiously monitor the quality of connection"""
import csv
import logging
import subprocess
from datetime import datetime
from os import path
from time import sleep

log = logging.getLogger(__name__)


def write_output(file_name: str, data: list):
    with open(file_name, "a") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            datetime.now().timestamp(),
            *data
        ])


def db_reading():
    """Reads how strong the connection is in dB"""
    with open("/proc/net/wireless") as f:
        return float(f.readlines()[2].split()[3])


def latency(host: str):
    """Get the latency from a single ping to host"""
    output = subprocess.run(
        ["ping", "-i", "1", "-c", "5", "-I", "wlan0", f"{host}"],
        capture_output=True
    ).stdout.decode()

    # This seemed like the easiest way to get the latency of the single ping.
    # This grabs the "min" from the statistics on the last line of "ping".
    # Lazy and stupid, but hey it's science.
    return float(output.splitlines()[-1].split()[-2].split("/")[0])


def measure():
    log.info("===== Starting data collection =====")
    while True:
        sleep(1)
        try:
            write_output(
                path.expanduser("~pi/client_measurement.csv"),
                [db_reading(), latency("192.168.4.1")]
            )
        except IndexError as e:
            log.warning(
                "Measurement Error: Couldn't read dB or latency.\n"
                "You're probably not connected to a network. This mostly "
                "happens if you just booted your device."
            )


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s][%(name)s][%(levelname)s]: %(message)s"
    )
    try:
        measure()
    except Exception as e:
        log.exception(e)
