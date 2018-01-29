#!/bin/sh
echo "setupwifi script started"
echo "copy file"
cp "wpa_supplicant_temp.conf" "/etc/wpa_supplicant/supplicant_test.conf"

echo "rebooting"
sleep 5s
reboot
