from wifi_scanner.scan import scan


def main():
    access_points = scan()

    for ap in access_points:
        print(ap)


if __name__ == "__main__":
    main()
