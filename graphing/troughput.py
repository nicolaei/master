from datetime import datetime
from typing import Tuple, List, Dict

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.axes import Subplot

from graphing.utils import avg_troughput_chuncked


def _modify_axis(
    ax: Subplot,
    time: list,
    data: list,
    *,
    color: str,
    label: str,
):
    ax.set_ylabel(label, color=color)
    if isinstance(time[0], list):
        for plot in zip(time, data):
            ax.plot(*plot)
    else:
        ax.plot(time, data, color=color)
    ax.tick_params(axis='y', labelcolor=color)

    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))


def troughput_graph(
    client_data: Tuple[List, List, List, List],
    ap_data: List[Dict],
    *,
    limit: Tuple[datetime, datetime] = None,
    title: str = None,
):
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()  # instantiates a second axes that shares the same x-axis

    ax1.set_xlabel('Time')

    start_time = client_data[1]
    decibels = client_data[3]
    troughput = avg_troughput_chuncked(
        zip(client_data[0], client_data[1], client_data[2]),
        chunck_size=5
    )

    print(f"Min avg Troughput: {min(troughput) / 10**6} MB/s")
    print(f"Max avg Troughput: {max(troughput) / 10**6} MB/s")

    _modify_axis(
        ax2, start_time[::5], troughput, color="tab:blue", label="Goodput (bytes)"
    )

    if limit:
        ax1.set_xlim(*limit)

    # Mark every time we've initiated a scan
    for data_point in ap_data:
        plt.axvline(x=data_point["time"])

    fig.suptitle(title)
    fig.set_size_inches(30, 10)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()
