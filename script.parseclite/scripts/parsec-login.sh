#!/bin/bash

#Close the media center
sudo openvt -c7 -s -f echo "Closing the media center..."
sudo openvt -c7 -s -f echo ""
sudo systemctl stop mediacenter

#Remove previous Parsec login
sudo openvt -c7 -s -f echo "Removing the previous Parsec login..."
sudo openvt -c7 -s -f echo ""
sudo rm -f /root/.parsec/user.bin
sudo rm -f /root/.parsec/lock

sleep 2

#Launch and log in to Parsec
sudo openvt -c7 -s -f echo "Trying to log in to Parsec, please connect a keyboard."
sudo openvt -c7 -s -f echo "Login attempt will automatically timeout in 60 seconds."
sudo openvt -c7 -s -f echo ""
sudo timeout 60 openvt -c7 -s -f -w -- parsecd

sleep 2

#Open the media center
sudo openvt -c7 -s -f echo "Opening media center and Parsec Lite..."
sudo openvt -c7 -s -f echo ""
sudo systemctl restart mediacenter

sleep 8

#Open parsec add-on
sudo kodi-send --action="Notification(Parsec Lite, Opening Parsec Lite)"
sudo kodi-send --action="RunAddon(script.parseclite)"

#Close the script
exit