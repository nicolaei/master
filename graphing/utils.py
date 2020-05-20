import csv
import json
from datetime import datetime
from itertools import islice
from pathlib import Path
from typing import List, Dict, Tuple, Iterable

from wifi_scanner.scan import AccessPoint


def client_data(file: Path) -> Tuple[List, List, List, List]:
    """Gets data from a client csv file

    :param file: The file to read
    """
    bytes_sent = []
    start_time = []
    end_time = []
    decibels = []

    with open(file) as f:
        # Sometimes the client will write a NULL on a line. Typically around the
        # end when the unit is powered off. These lines can safely be ignored.
        reader = csv.reader(line for line in f if "\0" not in line)

        for row in reader:
            bytes_sent.append(int(row[0]))
            start_time.append(datetime.fromtimestamp(float(row[1])))
            end_time.append(datetime.fromtimestamp(float(row[2])))
            decibels.append(float(row[3]))

    return bytes_sent, start_time, end_time, decibels


def access_point_data(file: Path) -> List[Dict]:
    """Gets data from an access point JSON file

    :param file: The file to read
    """
    with open(file) as f:
        data = json.load(f)

    return [
        {
            "time": datetime.fromtimestamp(item["time"]),
            "aps": [AccessPoint(**ap) for ap in item["aps"]]
        }
        for item in data
    ]


def timing_data(file: Path) -> List[Dict]:
    """Gets timing data from an access point JSON file

    NOTE: This is for the later access point measurements where I remembered
          to record _both_ start and end time.

    :param file: The file to read
    """
    with open(file) as f:
        data = json.load(f)

    return [
        {
            "start_time": datetime.fromtimestamp(item["start_time"]),
            "end_time": datetime.fromtimestamp(item["end_time"]),
        }
        for item in data
    ]


def _chunk(iterable: iter, chunck_size: int):
    """Returns the iterable split into chunck_size partitions.

    If the last partition is smaller than chunck_size, it will be shorter than
    chunck_size.
    """
    iterable = iter(iterable)
    return iter(lambda: tuple(islice(iterable, chunck_size)), ())


def calculate_troughput(bytes_: int, before: datetime, after: datetime) -> float:
    """Calculates the trougphut of a single transmision

    :returns: Troughput in bytes/s
    """
    return bytes_ / (after - before).total_seconds()


def avg_troughput_chuncked(
    data: Iterable[Tuple[int, datetime, datetime]], chunck_size: int
):
    """Get's the average troughput within chunck_size of items"""
    trougphuts = (calculate_troughput(*item) for item in data)

    return [
        sum(part) / len(part) for part in _chunk(trougphuts, chunck_size)
    ]
