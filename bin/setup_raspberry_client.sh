#!/usr/bin/env bash
# Setup for blank installations of Raspbian.
# Run this file as root on the RPi itself.

# Once ran, it will:
#  * Change the hostname to the specified one.
#  * Connect to the SSID

if [ -z "${3}" ]; then
    echo "Error: Not enough arguments! Usage: ${0} <hostname> <SSID> <ip>"
    exit 1
fi

apt install ntp ntpdate --yes

# Sometimes the time is wrong, which will affect our graphs
ntpdate -s time.google.com

echo "Changing hostname to ${1}! After this process is done connect to the"\
     "client with the hostname ${1}.local"

echo "${1}" > /etc/hostname

# Make the logger run at startup
echo "@reboot root cd ~pi/ && python3 -m troughput_tester.client 1>> /home/pi/cli.log 2>&1" > /etc/crontab

echo "
interface wlan0
  static ip_address=${3}/24
" >> /etc/dhcpcd.conf

echo "
network={
  ssid=\"${2}\"
  psk=\"TestingStuff\"
}" >> /etc/wpa_supplicant/wpa_supplicant.conf

service dhcpcd restart
wpa_cli -i wlan0 reconfigure

# wlan0 seems to be initially softblocked for some reason :/
rfkill unblock 0

reboot
