Master Thesis
=============

This repository contains everything conserning my master thesis.

Setting up Raspberry Pi
-----------------------

There are two files for setting up your Raspberry Pi:

 - `setup_raspberry_access_point.sh` for setting up as an access-point.
 
 - `setup_raspberry_client.sh` for setting up clients that connect to 
    access-points.

These have to be run as root. For headless clients, make sure to enable SSH
access by adding a file called `ssh` to the boot partition of the Pi.

Now we can initialize the pi. Start of by moving the files over:
```bash
scp -r bin client_logger wifi_scanner pi@raspberrypi.local:~/
```

Then run the client or access point setup script:
```bash
ssh pi@raspberrypi.local "sudo bash ~pi/bin/setup_raspberry_[client|access_point].sh"
```
The default password is `raspberry`.

If setting up the AP, the password will be `TestingStuff` and the access-points 
SSID will be the hostname.
