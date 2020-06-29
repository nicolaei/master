from math import log10
from statistics import mean
from typing import Tuple, Dict, List, Iterable

import numpy
import matplotlib.pyplot as plt
from scipy import stats

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


def group_by_decibels(data: Iterable[Dict]) -> Dict[float, AccessPoint]:
    discovered_access_points = {}

    for scan in data:
        for ap in scan["aps"]:
            discovered_access_points.setdefault(ap.signal_strength, []).append(ap)

    return discovered_access_points


def dbm_to_mw(measurement):
    """Convert from dBm to milli watts"""
    return 10 ** (measurement / 10.)


def dbm_to_snr(measurements: List[float], noise_power: float = -90):
    """Converts a list of dBm measurements to signal-to-noise measurements

    :param measurements: Measurements in dBm
    :param noise_power: Noise floor in dBm
    :returns: SNR in dB
    """

    noise_power = dbm_to_mw(noise_power)

    measurements_in_milli_watt = [
        dbm_to_mw(measurement) for measurement in measurements
    ]

    return [
        10 * log10(signal_power / noise_power)
        for signal_power in measurements_in_milli_watt
    ]


def detection_histogram(
    access_point_data: Tuple,
):
    """Creates a graph that shows the probability of discovery based on decibels

    :param access_point_data: Multiple access point data sets from different access points
    """
    db_sorted = [(len(scan), group_by_bss(scan)) for scan in access_point_data]

    fig, axs = plt.subplots(ncols=len(db_sorted), nrows=5, figsize=(28, 12))

    for index, (amount, aps) in enumerate(db_sorted):
        sorted_aps = sorted(
            aps.values(),
            key=len,
            reverse=True
        )
        for measure_index, ap_measurements in enumerate(list(sorted_aps)[:5]):
            axs[measure_index][index].hist(
                [ap.signal_strength for ap in ap_measurements],
                12
            )
            axs[measure_index][index].set_title(
                f"AP {index} - Top Measurement {measure_index}"
            )
            axs[measure_index][index].set_xlim(-90, -30)

    for ax in axs.flat:
        ax.set(xlabel="Signal Strength (dB)", ylabel="Number of discoveries")

    plt.show()
