#!/bin/bash

#Close the media center
sudo openvt -c7 -s -f echo "Closing the media center..."
sudo openvt -c7 -s -f echo ""
sudo systemctl stop mediacenter

#Install the Parsec client
sudo openvt -c7 -s -f echo "Adding Moonlight apt sources..."
sudo openvt -c7 -s -f echo ""
sudo echo "deb http://archive.itimmer.nl/raspbian/moonlight $(lsb_release -c -s) main" > /etc/apt/sources.list.d/moonlight.list

sudo openvt -c7 -s -f echo "Installing the Moonlight key..."
sudo openvt -c7 -s -f echo ""
sudo wget http://archive.itimmer.nl/itimmer.gpg
sudo apt-key add itimmer.gpg

sudo openvt -c7 -s -f echo "Installing the Moonlight client, this may take several minutes..."
sudo openvt -c7 -s -f echo ""
sudo apt-get update -y
sudo apt-get install -y moonlight-embedded

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