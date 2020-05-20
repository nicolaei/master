from datetime import timedelta
from statistics import mean
from typing import List, Dict

import matplotlib.pyplot as plt


def _time_taken(data: List[Dict]):
    return [item["end_time"] - item["start_time"] for item in data]


def scan_time(timings: dict):
    """A bar graph that shows how long time each scan takes

    :param timings: All timing measurements where the key is the scan name and
                    value is a list of measurements.
    """
    labels = ["Min Duration", "Max Duration", "Mean Duration"]
    label_index = list(range(len(labels)))
    bar_width = 1 / len(labels)

    fig, ax = plt.subplots(figsize=(10, 8))

    bars = []
    for index, (label, values) in enumerate(timings.items()):
        taken = _time_taken(values)
        timings = (
            min(taken).total_seconds(),
            max(taken).total_seconds(),
            (sum(taken, timedelta()) / len(taken)).total_seconds()
        )
        bars.append(
            ax.bar(
                [
                    i - bar_width / 2 + index / len(timings) * bar_width
                    for i in label_index
                ],
                timings,
                width=bar_width / len(timings),
                label=label
            )
        )

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel("Time in Seconds")
    ax.set_title("How long each scan takes")
    ax.set_xticks(label_index)
    ax.set_xticklabels(labels)
    ax.legend()

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f"{height:.2f}",
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 0),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    for bar in bars:
        autolabel(bar)

    plt.show()
