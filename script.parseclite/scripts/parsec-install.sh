#!/bin/bash

#Close the media center
sudo openvt -c7 -s -f echo "Closing the media center..."
sudo openvt -c7 -s -f echo ""
sudo systemctl stop mediacenter

#Install the Parsec client
sudo openvt -c7 -s -f echo "Downloading the Parsec client..."
sudo openvt -c7 -s -f echo ""
sudo wget https://s3.amazonaws.com/parsec-build/package/parsec-rpi.deb

sudo openvt -c7 -s -f echo "Installing the Parsec client, this may take several minutes..."
sudo openvt -c7 -s -f echo ""
sudo dpkg -i parsec-rpi.deb

sudo openvt -c7 -s -f echo "Removing the Parsec installer..."
sudo openvt -c7 -s -f echo ""
sudo rm -f parsec-rpi.deb

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