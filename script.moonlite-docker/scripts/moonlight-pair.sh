#!/bin/bash
#UTF-8 / EOL LF

#Launch and pair moonlight
echo "Pairing with Moonlight streamer..."
echo ""
docker run --tty --volume home:/home/moonlight-user clarkemw/moonlight-embedded-raspbian pair $1

#Close script
exit