#!/bin/bash

#Close the media center
sudo openvt -c7 -s -f echo "Closing the media center..."
sudo openvt -c7 -s -f echo ""
sudo systemctl stop mediacenter

#Launch and pair moonlight
sudo openvt -c7 -s -f echo "Pairing with the Moonlight streamer,"
sudo openvt -c7 -s -f echo "Connection will timeout in 20 seconds."
sudo timeout 20 openvt -c7 -s -f -w -- moonlight pair "$1"

sleep 2

#Open the media center
sudo openvt -c7 -s -f echo "Opening media center and Moonlite..."
sudo openvt -c7 -s -f echo ""
sudo systemctl restart mediacenter

sleep 8

#Open moonlite add-on
sudo kodi-send --action="Notification(Moonlite, Opening Moonlite)"
sudo kodi-send --action="RunAddon(script.moonlite)"

#Close the script
exit