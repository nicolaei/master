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

To run the files, you simply ssh to the default address:
```bash
ssh pi@raspberrypi.local "sudo bash -s --" < \
    ./bin/setup_raspberry_client.sh <hostname> <AP password>
```
The default password is `raspberry`.

If setting up the AP, the password will be `TestingStuff` and the access-points 
SSID will be the hostname.
