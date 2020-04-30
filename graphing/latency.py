from datetime import datetime
from typing import Tuple, List, Dict

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.axes import Subplot


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


# FIXME: There is something wrong. The data from the client isn't showing up.
def latency_graph(
    client_data: Tuple[List, List, List, List],
    ap_data: List[Dict],
    *,
    limit: Tuple[datetime, datetime] = None,
    title: str = None,
):
    """A graph to show how latency is affected by the scanning measurements

    The resulting graph has the latency on the Y axis and time on the X axis.

    :param client_data: All measurement data from a given client
    :param ap_data: Measurement data from the access point the client was connected to
    :param limit: A range of data to draw. Usefull for drawing a subset of the data.
    :param title: The title of the resulting graph
    """
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()  # instantiates a second axes that shares the same x-axis

    ax1.set_xlabel('Time')

    start_time = client_data[1]
    decibels = client_data[3]
    round_trip_time = [
        (after - before).total_seconds() * 1000
        for before, after in zip(client_data[1], client_data[2])
    ]

    _modify_axis(ax1, start_time, decibels, color="tab:red", label="dB")
    _modify_axis(
        ax2, start_time, round_trip_time, color="tab:green", label="Latency (ms)"
    )

    ax2.set_ylim(0, 250)
    if limit:
        ax1.set_xlim(*limit)

    # Mark every time we've initiated a scan
    for data_point in ap_data:
        plt.axvline(x=data_point["time"])

    fig.suptitle(title)
    fig.set_size_inches(30, 10)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()
