import json
import logging
from os import path
from json.decoder import JSONDecodeError
from functools import partial
from sys import argv
from datetime import timedelta, datetime

from wifi_scanner.algorithms import smooth_scan, full_scan, selective_scan
from wifi_scanner.schedulers import random_trigger, interval_trigger, \
    traffic_trigger, repeat_scan

log = logging.getLogger(__name__)


def write_output(
    file_name: str, start_time: datetime, end_time: datetime, access_points: list
):
    try:
        with open(file_name, "r") as json_file:
            data = json.load(json_file)
    except (JSONDecodeError, FileNotFoundError) as e:
        log.exception(e)
        log.warning("The file was empty; initializing with empty list!")
        data = []

    data.append(
        {
            "start_time": start_time.timestamp(),
            "end_time": end_time.timestamp(),
            "aps": [
                {
                    "bss": ap.bss,
                    "ssid": ap.ssid,
                    "frequency": ap.frequency,
                    "signal_strength": ap.signal_strength
                }
                for ap in access_points
            ]
        },
    )

    with open(file_name, "w") as json_file:
        json.dump(data, json_file)


algorithms = {
    "full": full_scan,
    "selective": partial(selective_scan, channels=[1, 6, 11]),
    "selective_1ch": partial(selective_scan, channels=[1]),
    "selective_odd": partial(selective_scan, channels=[1, 3, 5, 7, 9, 11]),
    "smooth_300": partial(smooth_scan, interval=timedelta(milliseconds=300)),
    "smooth_600": partial(smooth_scan, interval=timedelta(milliseconds=600)),
    "smooth_1200": partial(smooth_scan, interval=timedelta(milliseconds=1200)),
}

schedulers = {
    "single": partial(repeat_scan, repetitions=1),
    "5min": partial(interval_trigger, interval=timedelta(minutes=5)),
    "2min": partial(interval_trigger, interval=timedelta(minutes=2)),
    "traffic": traffic_trigger
}

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s][%(name)s][%(levelname)s]: %(message)s"
    )

    # This could use Argparse, but that's really overcomplicating this simple
    # usecase.
    if len(argv) < 3:
        print(f"Not enough arguments! "
              f"Usage: {argv[0]} <scanning algorithm> <scheduler>")
        exit(1)
    elif argv[1] not in algorithms.keys():
        print(f"Invalid scanning algorithm '{argv[1]}'. "
              f"Choose from: {', '.join(algorithms.keys())}")
        exit(1)
    elif argv[2] not in schedulers.keys():
        print(f"Invalid scheduler '{argv[2]}'. "
              f"Choose from: {', '.join(schedulers.keys())}")
        exit(1)

    algorithm = algorithms[argv[1]]
    scheduler = schedulers[argv[2]]

    log.info(f"===== Starting {argv[2]} with {argv[1]} scan =====")
    for start_time, end_time, scan in scheduler(algorithm):
        write_output(
            path.expanduser("~pi/scanner_measurements.json"),
            start_time,
            end_time,
            list(scan)
        )
