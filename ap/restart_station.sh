#!/bin/sh
#
cp dhcpcd.conf.station /etc/dhcpcd.conf
cp interfaces.station /etc/network/interfaces
systemctl disable hostapd
shutdown -r now
