#!/bin/bash
#UTF-8 / EOL LF

#Launch and list moonlight apps
sudo openvt -c7 -s -f echo "Listing Moonlight streamer apps..."
sudo openvt -c7 -s -f echo ""
sudo timeout 5 moonlight list "$1"

#Close the script
exit