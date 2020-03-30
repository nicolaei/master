#!/usr/bin/env python3
"""Continiously monitor the quality of connection"""
import asyncio
import csv
import logging
import re
from datetime import datetime
from os import path

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


async def latency(
    host: str,
    interval: float = 0.25,
    timeout: float = 0.25,
    interface: str = "wlan0",
):
    """Get the latency to a host every interval

    :param host: The host to check against
    :param interval: The amount of time between each ping request in seconds
    :param timeout: The max amount of time to wait for a response in seconds.
    :param interface: The interface to do the request on.
    """
    process = await asyncio.create_subprocess_shell(
        f"ping -O -i {interval} -W {timeout} -I {interface} {host}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    # Ping always prints one info line. This line should be ignored.
    await process.stdout.readline()

    while True:
        stdout = (await process.stdout.readline()).decode("utf-8")
        if stdout.startswith("no answer yet for"):
            yield None
        else:
            yield float(re.search(r"(?<=time=)\S+(?= ms)", stdout).group())


async def measure():
    log.info("===== Starting data collection =====")

    async for ping in latency("192.168.4.1"):
        try:
            signal_strength = db_reading()
        except IndexError:
            log.warning(
                "Measurement Error: Couldn't read dB or latency.\n"
                "You're probably not connected to a network. This mostly "
                "happens if you just booted your device."
            )
            continue

        write_output(
            path.expanduser("~pi/client_measurement.csv"),
            [signal_strength, ping]
        )


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s][%(name)s][%(levelname)s]: %(message)s"
    )
    try:
        asyncio.run(measure())
    except Exception as e:
        log.exception(e)
