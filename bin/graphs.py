
import csv
import json
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def draw(folder: str):
    time = []
    db = []
    latency = []
    with open(f"./measurements/{folder}/client_measurement.csv") as f:
        reader = csv.reader(f)
        for row in reader:
            time.append(datetime.fromtimestamp(float(row[0])))
            db.append(float(row[1]))
            latency.append(float(row[2]))

    with open(f"./measurements/{folder}/scanner_measurements.json") as f:
        data = json.load(f)

    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Time')
    ax1.set_ylabel('dB', color=color)
    ax1.plot(time, db, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    color = 'tab:green'
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('Latency', color=color)  # we already handled the x-label with
    ax2.plot(time, latency, color=color)
    ax2.tick_params(axis='y', labelcolor=color)


    ax1.set_xlim(
        datetime(year=2020, month=3, day=7, hour=0, minute=0, second=0),
        datetime(year=2020, month=3, day=7, hour=1, minute=0, second=0)
    )
    ax2.set_ylim(0, 5)

    ax1.xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
    ax2.xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

    [plt.axvline(x=datetime.fromtimestamp(float(data_point["time"])))
     for data_point in data]

    fig.set_size_inches(30, 10)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()


draw("full_5min_far")
