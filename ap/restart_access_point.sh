 #!/bin/sh
#
cp dhcpcd.conf.access_point /etc/dhcpcd.conf
cp interfaces.access_point /etc/network/interfaces
systemctl enable hostapd.service
systemctl enable isc-dhcp-server.service
systemctl disable wpa_supplicant.service 
#shutdown -r now
 
systemctl stop wpa_supplicant.service &&  systemctl start hostapd.service && systemctl start isc-dhcp-server.service 
shutdown -r now
