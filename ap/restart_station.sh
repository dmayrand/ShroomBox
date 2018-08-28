 #!/bin/sh
#
cp dhcpcd.conf.station /etc/dhcpcd.conf
cp interfaces.station /etc/network/interfaces
systemctl disable hostapd.service
systemctl disable isc-dhcp-server.service
systemctl enable wpa_supplicant.service 
#shutdown -r now
 
systemctl stop hostapd.service && systemctl stop isc-dhcp-server.service && systemctl start wpa_supplicant.service
shutdown -r now
