#!/bin/sh
#
cp dhcpcd.conf.access_point /etc/dhcpcd.conf
cp interfaces.access_point /etc/network/interfaces
systemctl enable hostapd
shutdown -r now
