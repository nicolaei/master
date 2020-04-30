import logging
from pathlib import Path
from typing import List, Tuple

from graphing.latency import latency_graph
from graphing.scan_accuracy import accuracy_graph
from graphing.utils import client_data, access_point_data


logger = logging.getLogger(__name__)


def render_graphs(folders: List[Tuple[Path, str]]):
    """Renders all relevant graphs for the given folder

    :param folders: A list of folders and the name of which scan they contain
    """
    for folder, scan_name in folders:
        logger.info(f"Loading data for {scan_name}")

        try:
            client_0 = client_data(folder / "client_0_measurements.csv")
            client_2 = client_data(folder / "client_2_measurements.csv")
            ap_0 = access_point_data(folder / "scanner_0_measurements.json")
            ap_1 = access_point_data(folder / "scanner_1_measurements.json")
            ap_2 = access_point_data(folder / "scanner_2_measurements.json")
        except FileNotFoundError as e:
            logger.warning(f"Couldn't find {e.filename}. Continuing to next scan type")
            continue

        time_range = [client_0[1][10000], client_0[1][50000]]

        logger.info(f"Creating graphs for {scan_name}")

        latency_graph(client_0, ap_0, title=scan_name, limit=time_range)
        latency_graph(client_2, ap_2, title=scan_name, limit=time_range)
        # TODO: These should probably be named after which AP they are
        accuracy_graph(ap_0, title=f"{scan_name} (AP0)")
        accuracy_graph(ap_1, title=f"{scan_name} (AP1)")
        accuracy_graph(ap_2, title=f"{scan_name} (AP2)")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s][%(name)s][%(levelname)s]: %(message)s"
    )
    render_graphs([
        (Path("./measurements/full"), "Full Scan"),
        (Path("./measurements/selective_1_7_11"), "Selective Scan (Ch 1,7,11)"),
        (Path("./measurements/selective_even"), "Selective Scan (Every other channel)"),
        (Path("./measurements/smooth_300"), "Smooth Scan (300ms)"),
        (Path("./measurements/smooth_600"), "Smooth Scan (600ms)"),
        (Path("./measurements/smooth_1200"), "Smooth Scan (1200ms)"),
    ])
