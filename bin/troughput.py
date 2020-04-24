import csv
from datetime import datetime
from itertools import islice
from statistics import mean


def _client_data(folder: str, file: str):
    bytes_recieved = []
    rtts = []
    before_time = []
    after_time = []

    with open(f"{folder}/{file}") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            if row[1] == "-1.0":
                # TODO: This is only while testing.
                continue
            bytes_recieved.append(int(row[0]))
            before_time.append(datetime.fromtimestamp(float(row[1])))
            after_time.append(datetime.fromtimestamp(float(row[2])))

            rtts.append(float(row[2]) - float(row[1]))

    return bytes_recieved, rtts, before_time, after_time


def chunk(iterable, chunck_size):
    iterable = iter(iterable)
    return iter(lambda: tuple(islice(iterable, chunck_size)), ())


def main():
    b, r, bt, rt = _client_data(
        "../measurements/test/", "client_measurements.csv")

    all_troughputs = [
        data / (after-before).total_seconds()
        for data, before, after in zip(b, bt, rt)
    ]
    # Get the average for 1000 fetches. Should be over a period in stead!
    troughput_avg_1000 = [
        sum(part) / len(part) for part in chunk(all_troughputs, 1000)
    ]
    all_bytes = sum(b)
    all_rtts = sum(r)
    max_rtt = max(r)


    # By only looking at RTT, we omit the overhead my client code introduces
    print(f"Min avg Troughput: {min(troughput_avg_1000) / 10**6} MB/s")
    print(f"Max avg Troughput: {max(troughput_avg_1000) / 10**6} MB/s")
    print(f"All Troughput: {(all_bytes / all_rtts) / 10**6} MB/s")
    print(f"Average RTT: {(all_rtts / len(r)) * 10**3} ms")
    print(f"Max RTT: {(max_rtt) * 10**3} ms")


if __name__ == "__main__":
    main()
