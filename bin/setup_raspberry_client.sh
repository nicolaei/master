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

echo "Changing hostname to ${1}! After this process is done connect to the"\
     "client with the hostname ${1}.local"

echo "${1}" > /etc/hostname

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

reboot
