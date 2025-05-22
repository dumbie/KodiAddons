#!/bin/bash
#UTF-8 / EOL LF
. /etc/profile

#Close media center
echo "Closing media center..."
echo ""
systemctl stop kodi

#Launch and stream moonlight
echo "Connecting to Moonlight streamer..."
docker run --volume home:/home/moonlight-user --device /dev/vchiq --device /dev/input clarkemw/moonlight-embedded-raspbian stream $1 -1080 -app $2 -fps 60 -bitrate 20000 -localaudio

sleep 2

#Open media center
echo "Opening media center and Moonlite..."
echo ""
systemctl restart kodi

sleep 8

#Open moonlite add-on
kodi-send --action="Notification(Moonlite, Opening Moonlite)"
kodi-send --action="RunAddon(script.moonlite-docker)"

#Close script
exit