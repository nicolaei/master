import csv
from datetime import datetime


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
            bytes_recieved.append(int(row[0]))
            before_time.append(datetime.fromtimestamp(float(row[1])))
            after_time.append(datetime.fromtimestamp(float(row[2])))

            rtts.append(float(row[2]) - float(row[1]))

    return bytes_recieved, rtts, before_time, after_time


def main():
    b, r, bt, rt = _client_data(".", "lol.csv")

    all_bytes = sum(b)
    all_rtts = sum(r)

    # By only looking at RTT, we omit the overhead my client code introduces
    print(f"Troughput: {(all_bytes / all_rtts) / 10**6} MB/s")
    print(f"Average RTT: {(all_rtts / len(r)) * 10**3} ms")


if __name__ == "__main__":
    main()
