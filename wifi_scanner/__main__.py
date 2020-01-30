import logging
from datetime import timedelta
from timeit import default_timer as timer

from wifi_scanner.algorithms import smooth_scan


log = logging.getLogger(__name__)


def main():
    log.info("Starting smooth scan")

    start = timer()
    access_points = smooth_scan(timedelta(milliseconds=300))
    end = timer()

    log.info(f"Found {len(access_points)} access points "
             f"in {end - start:.2f} sec!")
    for ap in access_points:
        print(ap)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s][%(name)s][%(levelname)s]: %(message)s"
    )
    main()
