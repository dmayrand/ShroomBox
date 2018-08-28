#!/bin/sh
#

echo "Starting up ShroomBox apps"
## start local server
sudo python3 shroomserver.py & 
cd ap
## start the listener of the button on  GPIO 26
sudo python3 resetbutton.py &
## start the main engine
cd ../../akcore
# sudo python3 divae.py
