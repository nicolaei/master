import json
from statistics import mean, stdev

import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

from wifi_scanner.scan import AccessPoint


def _ap_data(folder: str, file: str):
    with open(f"{folder}/{file}") as f:
        return json.load(f)


def orginize_data(data: dict) -> dict:
    """Orginizes the data for the graph

    :returns: The discovered APs, and the result for every time they were discovered.
              In addition, the total number of scans and total number of APs
    """
    discovered_access_points = {}

    for scan in data:
        for ap in scan["aps"]:
            discovered_ap = AccessPoint(**ap)
            discovered_access_points.setdefault(ap["bss"], []).append(discovered_ap)

    return discovered_access_points


def get_x_y_asymetric_variance(data):
    """Gets the data ready for plotting with asymetric errors"""
    times_discoveries = []
    db = []
    low_db_variance = []
    high_db_variance = []

    for bss, discoveries in data.items():
        if len(discoveries) < 2:
            # Some APs just pass by
            continue

        times_discoveries.append(len(discoveries))

        signal_strengths = [d.signal_strength for d in discoveries]
        db.append(mean(signal_strengths))
        low_db_variance.append(mean(signal_strengths) - min(signal_strengths))
        high_db_variance.append(max(signal_strengths) - mean(signal_strengths))

    return times_discoveries, db, [low_db_variance, high_db_variance]


def get_x_y_stdev(data):
    """Gets the data ready for plotting with stdev as error"""
    times_discoveries = []
    db = []
    db_variance = []
    labels = []

    for bss, discoveries in data.items():
        if len(discoveries) < 2:
            # Some APs just pass by
            continue

        times_discoveries.append(len(discoveries))
        labels.append(discoveries[0].ssid)

        signal_strengths = [d.signal_strength for d in discoveries]
        db.append(mean(signal_strengths))
        db_variance.append(stdev(signal_strengths))

    return times_discoveries, db, db_variance, labels


def draw(
    folder: str,
    title: str = None,
):
    scans = _ap_data(folder, "scanner_measurements.json")
    scans = scans[:1000]
    discovered_aps = orginize_data(scans)
    times_discovered, db, db_variance, labels = get_x_y_stdev(discovered_aps)

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
        f"Access Points Discovered (Over {len(scans)} scans) ({title or folder})"
    )
    fig.set_size_inches(30, 12)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()


if __name__ == "__main__":
    draw("./measurements/full_5min", "Full Scan")
    draw("./measurements/selective_1ch_5min", "Selective Scan (Ch 1)")
    draw("./measurements/selective_5min", "Selective Scan (Ch 1,7,11)")
    draw("./measurements/smooth_300_5min", "Smooth Scan (300ms)")
    draw("./measurements/smooth_600_5min", "Smooth Scan (600ms)")
    draw("./measurements/smooth_1200_5min", "Smooth Scan (1200ms)")
