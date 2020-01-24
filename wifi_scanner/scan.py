import subprocess
from dataclasses import dataclass


FREQUENCY_CHANNEL = {
    **{2412 + (channel - 1) * 5: channel for channel in range(1, 14)},
    2484: 14
}
"""All channels in the 2.4Ghz space.

Every channel, except 14, is spaced 5 MHz appart. Starting from 2412 MHz.
"""


def first_occurance(prefix: str, lines: list):
    """Gets the first occurance of prefix in lines"""
    return next(line[len(prefix):]
                for line in lines
                if line.startswith(prefix))


@dataclass
class AccessPoint:
    bss: str
    ssid: str
    frequency: int
    signal_strength: float

    @property
    def channel(self):
        return FREQUENCY_CHANNEL[self.frequency]

    @classmethod
    def from_iw_scan(cls, scan_result: str):
        """Naive parsing of a single BSS

        Expects that the "BSS" in the start of each result is stripped away.
        """
        split_result = scan_result.splitlines()

        bss = split_result[0][:17]
        ssid = first_occurance("\tSSID: ", split_result)
        freq = int(first_occurance("\tfreq: ", split_result))
        signal = float(first_occurance("\tsignal: ", split_result).split()[0])

        return cls(bss, ssid, freq, signal)

    def __str__(self):
        return f"{self.ssid} (on channel {self.channel} " \
               f"at {self.signal_strength} dBm)"


def scan_with_iw(frequency: int = None):
    """Grab the results of a scan from the iw tool.

    :param frequency: Frequency to scan, if left empty all channels
                      will be scanned.
    """
    command = ["iw", "wlan0", "scan"] if not frequency \
        else ["iw", "wlan0", "scan", "frequency", f"{frequency}"]

    output = subprocess.run(command, capture_output=True)
    return output.stdout.decode()


def parse_scan_result(scan: str):
    """Naive parsing of the output from iw scan"""
    results = scan.split("\nBSS ")
    results[0] = results[0][4:]  # The first occurance doesn't remove "BSS".

    return [AccessPoint.from_iw_scan(bss) for bss in results]


def main():
    scan_result = scan_with_iw()
    access_points = parse_scan_result(scan_result)
    for ap in access_points:
        print(ap)


if __name__ == "__main__":
    main()
