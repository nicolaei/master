import logging
from datetime import timedelta

from wifi_scanner.algorithms import smooth_scan


log = logging.getLogger(__name__)


def main():
    log.info("Starting smooth scan")
    access_points = smooth_scan(timedelta(milliseconds=300))

    log.info(f"Found {len(access_points)} access points!")
    for ap in access_points:
        print(ap)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s][%(name)s][%(levelname)s]: %(message)s"
    )
    main()
