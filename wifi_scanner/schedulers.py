"""All the scheduling methods for the experiment

These are all generators to enable easy extraction of the scanning data.
"""
import logging
from datetime import timedelta
from time import sleep

log = logging.getLogger(__name__)


def repeat_scan(
    scanner: callable,
    repetitions: int,
    include_all_results: bool = False
):
    """Repeats the given scan multiple times

    :param scanner: A function that returns a set of access points.
    :param repetitions: The amount of times to run the given scanner.
    :param include_all_results: Returns the results of every individual scan
                                in addition to the main result.
    :returns: All the discovered access points, and the result of each
              individual scan (if include_all_results is True).
    """
    discovered_access_points = set()

    results = []
    for i in range(repetitions):
        log.debug(f"Starting scan {i}.")
        found = scanner()

        results.append(found)
        discovered_access_points |= found

    if include_all_results:
        return discovered_access_points, results
    else:
        return discovered_access_points


def interval_trigger(scanner: callable, interval: timedelta):
    """Triggers the scanner every interval."""
    while True:
        log.info("Triggering Scan")
        yield scanner()

        log.info(f"Sleeping for {interval}")
        sleep(interval.total_seconds())


def random_trigger(scanner: callable):
    """Triggers the scan at a random time

    :param scanner: A function that returns a set of access points.
    :returns: A set of access points
    """
    raise NotImplementedError()


def traffic_trigger(
    scanner: callable,
    treshold: int,
    backoff_period: timedelta = timedelta(minutes=30)
):
    """Triggers the scan based on the amount of traffic on the network

    :param scanner: A function that returns a set of access points.
    :param treshold: The treshold (in dBm) when a scan should trigger.
    :param backoff_period: A given amount of time to wait before the next scan.
                           This ensures that the access point won't flood the
                           network with PRs in periods of low traffic.
    :returns: A set of access points
    """
    raise NotImplementedError()
