import logging
from datetime import timedelta
from time import sleep

from wifi_scanner.scan import CHANNEL_FREQUENCY, scan


log = logging.getLogger(__name__)


def full_scan():
    """A simple scan of all channels, concecutivelly"""
    channel = {ch: freq for ch, freq in CHANNEL_FREQUENCY.items()}

    access_points = set()
    for channel, frequency in channel.items():
        found = scan(frequency)

        log.debug(f"Found {len(found)} APs on channel {channel}. "
                  f"{len(found & access_points)} of these were already "
                  f"discovered.")

        access_points |= found

    return access_points


def selective_scan(channels: list):
    """Only scan some channels on the network

    This approach aims to decrease the total time the scan takes.
    """
    selected = {ch: freq for ch, freq in CHANNEL_FREQUENCY.items()
                if ch in channels}

    access_points = set()
    for channel, frequency in selected.items():
        found = scan(frequency)

        log.debug(f"Found {len(found)} APs on channel {channel}. "
                  f"{len(found & access_points)} of these were already "
                  f"discovered.")

        access_points |= found

    return access_points


def smooth_scan(interval: timedelta, group_size: int = 1):
    """Scanning method that switches between scanning and normal operation"""
    # Stolen from "grouper" example in itertools documentation.

    access_points = set()
    for i, (channel, frequency) in enumerate(CHANNEL_FREQUENCY.items()):
        found = scan(frequency)

        log.debug(f"Found {len(found)} APs on channel {channel}. "
                  f"{len(found & access_points)} of these were already "
                  f"discovered.")

        access_points |= found

        if i % group_size is 0:
            log.debug(f"Reached group size ({group_size})! "
                      f"Sleeping for {interval}")
            sleep(interval.total_seconds())

    return access_points
