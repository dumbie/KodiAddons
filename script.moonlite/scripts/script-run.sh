#!/bin/bash
#UTF-8 / EOL LF

script_args="$(printf " %q " "$@")"

#Run the requested script
sudo openvt -c7 -s -f clear
sudo openvt -c7 -s -f echo "Running the requested script..."
sudo su -c "sh $script_args &" &

#Close the script
exit