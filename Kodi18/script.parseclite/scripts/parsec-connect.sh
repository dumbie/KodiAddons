#!/bin/bash

#Close the media center
sudo openvt -c7 -s -f echo "Closing the media center..."
sudo openvt -c7 -s -f echo ""
sudo systemctl stop mediacenter

#Launch and connect Parsec
sudo openvt -c7 -s -f echo "Connecting to Parsec host..."
sudo openvt -c7 -s -f echo ""
sudo openvt -c7 -s -f -w -- parsec "$1"

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