
import csv
import json
from datetime import datetime
from typing import Tuple, List

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.axes import Subplot


def _ap_data(folder: str, file: str):
    with open(f"{folder}/{file}") as f:
        return json.load(f)


def _client_data(folder: str, file: str):
    time = []
    db = []
    latency = []

    with open(f"{folder}/{file}") as f:
        reader = csv.reader(f)
        for row in reader:
            time.append(datetime.fromtimestamp(float(row[0])))
            db.append(float(row[1]))
            latency.append(float(row[2]))

    return time, db, latency


def _modify_axis(
    ax: Subplot,
    time: list,
    data: list,
    *,
    color: str,
    label: str,
):
    ax.set_ylabel(label, color=color)
    ax.plot(time, data, color=color)
    ax.tick_params(axis='y', labelcolor=color)

    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))


def draw(
    folder: str,
    limit: Tuple[datetime, datetime] = None,
    client_data: Tuple = None,
    ap_data: Tuple = None
):
    time, db, latency = client_data or _client_data(folder, "client_measurement.csv")
    ap_data = ap_data or _ap_data(folder, "scanner_measurements.json")

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    ax1.set_xlabel('Time')

    _modify_axis(ax1, time, db, color="tab:red", label="dB")
    _modify_axis(ax2, time, latency, color="tab:green", label="Latency")

    ax2.set_ylim(0, 5)
    if limit:
        ax1.set_xlim(*limit)

    # Mark every time we've initiated a scan
    [plt.axvline(x=datetime.fromtimestamp(float(data_point["time"])))
     for data_point in ap_data]

    fig.set_size_inches(30, 10)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()


draw(
    "./measurements/full_5min_far",
    limit=(
        datetime(year=2020, month=3, day=7, hour=0, minute=0, second=0),
        datetime(year=2020, month=3, day=7, hour=1, minute=0, second=0),
    ),
)

draw(
    "./measurements/full_5min_close",
    limit=(
        datetime(year=2020, month=3, day=8, hour=0, minute=0, second=0),
        datetime(year=2020, month=3, day=8, hour=1, minute=0, second=0),
    )
)

draw(
    "./measurements/smooth_5min_far",
    limit=(
        datetime(year=2020, month=3, day=9, hour=0, minute=0, second=0),
        datetime(year=2020, month=3, day=9, hour=1, minute=0, second=0)
    )
)

draw(
    "./measurements/smooth_5min_close",
    limit=(
        datetime(year=2020, month=3, day=12, hour=0, minute=0, second=0),
        datetime(year=2020, month=3, day=12, hour=1, minute=0, second=0)
    )
)
