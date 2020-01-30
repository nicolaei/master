import logging
from datetime import timedelta

from wifi_scanner.algorithms import smooth_scan


def main():
    access_points = smooth_scan(timedelta(milliseconds=300))

    for ap in access_points:
        print(ap)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s][%(name)s][%(levelname)s]: %(message)s"
    )
    main()
