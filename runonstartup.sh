#!/bin/sh
#

echo "Starting up ShroomBox apps"
#run local client
sudo python3 shroomserver.py & 
#run local input listener
cd ap
sudo python3 resetwifi.py &
#run diversity engine
