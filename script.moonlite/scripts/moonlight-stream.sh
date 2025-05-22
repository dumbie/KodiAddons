#!/bin/bash
#UTF-8 / EOL LF

#Close the media center
sudo openvt -c7 -s -f echo "Closing the media center..."
sudo openvt -c7 -s -f echo ""
sudo systemctl stop mediacenter

#Launch and connect moonlight
sudo openvt -c7 -s -f echo "Launching: $2"
sudo openvt -c7 -s -f echo "Connecting to Moonlight streamer..."
sudo openvt -c7 -s -f -w -- moonlight stream "$1" -app "$2" -width "$3" -height "$4" -bitrate "$5" -fps "$6" "$7" "$8" -unsupported

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