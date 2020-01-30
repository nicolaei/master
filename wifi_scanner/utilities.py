import logging


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
