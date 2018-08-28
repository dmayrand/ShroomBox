#!/bin/sh
echo "setupwifi script started"
echo "copy file"
cp "wpa_supplicant_temp.conf" "/etc/wpa_supplicant/wpa_supplicant.conf"
cd ap/
./restart_station.sh
echo "rebooting"
sleep 5s
reboot
