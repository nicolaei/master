#!/usr/bin/env bash
# Setup for blank installations of Raspbian.
# Run this file as root on the RPi itself.

# Once ran, it will:
#  * Change the hostname to the specified one.
#  * Set the IP to 192.168.4.1/24
#  * Setup hostapd with password Testing Stuff

if [ -z "${1}" ]; then
    echo "Error: No arguments supplied. Usage: ${0} <hostname>"
    exit 1
fi


echo "Changing hostname to ${1}! After this process is done connect to the"\
     "client with the hostname ${1}.local"
echo "${1}" > /etc/hostname

apt update --yes
apt install dnsmasq hostapd --yes

# Make the scanner run at startup
echo "@reboot python -m ~pi/wifi_scanner full 5min" >> /etc/crontab

# Setup the APs IP
echo "
interface wlan0
    static ip_address=192.168.4.1/24
    nohook wpa_supplicant
" >> /etc/dhcpcd.conf

# Create the config
echo "interface=wlan0
driver=nl80211
ssid=${1}
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=TestingStuff
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
ctrl_interface=/var/run/hostapd
ctrl_interface_group=0
" > /etc/hostapd/hostapd.conf

# Tell HOSTAPD where the config is
echo DAEMON_CONF="/etc/hostapd/hostapd.conf" > /etc/default/hostapd

# Restart dhcpd
service dhcpcd restart
# Enable and start hostapd
systemctl unmask hostapd
systemctl enable hostapd
systemctl start hostapd
systemctl status hostapd

# wlan0 seems to be initially softblocked for some reason :/
rfkill unblock 0

reboot
