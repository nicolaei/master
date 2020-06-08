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



def detection_probability(
    access_point_data: Tuple,
    title: str = None,
):
    """Creates a graph that shows the probability of discovery based on decibels

    :param access_point_data: Multiple access point data sets from different access points
    :param title: Title of the graph
    """
    db_sorted = [(len(scan), group_by_bss(scan)) for scan in access_point_data]

    ap_probabilities = {
        "Signal Strength (dB)": [],
        "Probability of Discovery": []
    }
    for amount, aps in db_sorted:
        for ap_measurements in aps.values():
            ap_probabilities["Signal Strength (dB)"].append(
                max(ap.signal_strength for ap in ap_measurements)
            )
            ap_probabilities["Probability of Discovery"].append(
                len(ap_measurements) / amount
            )

    ap_probabilities["Signal Strength (dB)"] = \
        dbm_to_snr(ap_probabilities["Signal Strength (dB)"])

    fig = plt.figure(figsize=(20, 12))

    plt.scatter(
        x=ap_probabilities["Signal Strength (dB)"],
        y=ap_probabilities["Probability of Discovery"],
        label="Discovered Access Point"
    )

    plt.xlabel("Signal Strength (dB SNR)")
    plt.ylabel("Probability of Discovery")

    x = numpy.linspace(stats.rayleigh.ppf(0.1), stats.rayleigh.ppf(0.99), 100)

    plt.plot(
        numpy.linspace(0, 60, 100),
        stats.rayleigh.cdf(x, loc=0.48, scale=0.8),
        "y",
        label="Rayleigh",
    )

    bessel = 0.1
    x = numpy.linspace(
        stats.rice.ppf(0.1, b=bessel), stats.rice.ppf(0.99, b=bessel), 100
    )

    plt.plot(
        numpy.linspace(0, 60, 100),
        stats.rice.cdf(x, loc=0.9, b=bessel, scale=0.4),
        "r",
        label="Rice"
    )

    plt.suptitle(
        f"Probability of discovery ({title})"
    )
    plt.legend()
    plt.show()
