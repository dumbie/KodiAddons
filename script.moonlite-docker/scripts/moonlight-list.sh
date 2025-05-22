#!/bin/bash
#UTF-8 / EOL LF

#Launch and list moonlight apps
echo "Listing Moonlight streamer apps..."
echo ""
docker run --volume home:/home/moonlight-user clarkemw/moonlight-embedded-raspbian list $1

#Close script
exit