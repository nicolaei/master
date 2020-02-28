#!/usr/bin/env python3
"""Continiously monitor the quality of connection"""
import csv
import logging
import subprocess
from datetime import datetime
from time import sleep


log = logging.getLogger(__name__)


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
        signal_strenght = db_reading()
        latency_ap = latency("192.168.4.1")

        with open("/tmp/client_measurement.csv", "a") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                datetime.now().timestamp(),
                signal_strenght,
                latency_ap
            ])


measure()
