from typing import List, Dict
from statistics import mean, stdev

import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

from wifi_scanner.scan import AccessPoint


def group_by_bss(data: dict) -> Dict[str, List[AccessPoint]]:
    """Orginizes the data for the graph

    This allows us to map out how many times an access point has been discovered.
    Even in, the extremly unlikely, cases where an access point may change name.

    :returns: The discovered APs, and the result for every time they were discovered.
              In addition, the total number of scans and total number of APs
    """
    discovered_access_points = {}

    for scan in data:
        for ap in scan["aps"]:
            discovered_access_points.setdefault(ap.bss, []).append(ap)

    return discovered_access_points


def get_x_y_stdev(data: Dict[str, List[AccessPoint]], *, asymetric: bool = False):
    """Gets the data ready for plotting with stdev as error"""
    times_discoveries = []
    db = []
    db_variance = [] if not asymetric else [[], []]
    labels = []

    for _, discoveries in data.items():
        if len(discoveries) < 2:
            # Some APs just pass by. They might be phones with WiFi hotspots.
            # They clutter up the resulting graph and arn't usefull, so they get
            # removed.
            continue

        times_discoveries.append(len(discoveries))

        labels.append(discoveries[0].ssid)

        signal_strengths = [d.signal_strength for d in discoveries]
        db.append(mean(signal_strengths))

        if asymetric:
            db_variance[0].append(mean(signal_strengths) - min(signal_strengths))
            db_variance[1].append(max(signal_strengths) - mean(signal_strengths))
        else:
            db_variance.append(stdev(signal_strengths))

    return times_discoveries, db, db_variance, labels


def accuracy_graph(
    ap_data: List[Dict],
    title: str = None,
):
    times_discovered, db, db_variance, labels = get_x_y_stdev(
        group_by_bss(ap_data[:100])
    )

    fig, ax1 = plt.subplots()

    ax1.errorbar(y=times_discovered, x=db, xerr=db_variance,
                 fmt=".k", marker="o")

    ax1.set_ylabel("Times Discovered")
    ax1.set_xlabel("Signal Strength (dB)")
    ax1.set_yscale("log")
    ax1.yaxis.set_major_formatter(ScalarFormatter())

    for x, y, name in zip(db, times_discovered, labels):
        ax1.annotate(name, (x, y))

    fig.suptitle(
        f"Access Points Discovered (Over {len(ap_data)} scans) ({title})"
    )
    fig.set_size_inches(30, 12)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()
