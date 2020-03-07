#!/bin/sh
# Script: SnowballBoot.sh
# Purpose: Helper script to launch Snowball after rebooting
# the Raspberry Pi. 
#
# Setup Steps:
# 0 - Copy to the /boot dir
# cp SnowballBoot.sh /boot/
# cd /boot
#
# 1 - Make exucutable 
# chmod 755 SnowballBoot.sh
#
# 2 - Add to crontb 
# sudo contrab -e
# @reboot sh path_to_this scrip
# 
# Ex. @reboot sudo sh /boot/SnowballBoot.sh > /home/pi/Desktop/snowball/cronlogs 2>&1
#
# 3 - Save changes
# Ctrl-O
#
# 4 - Exit
# Ctrl-X
#
# 5 - Reboot
# sudo reboot
#

# Start bluetooth.
sudo /etc/init.d/bluetooth restart

# Sleep for now to give the interface time to load.
# Need a better way to do this.
sleep 15

# Make HomePi discoverable.
sudo hciconfig hci0 piscan

# Change to your user home dir.
cd ~

# Change to Snowball root directory. 
# Note: You might need to change this depending on your location.
cd /home/pi/Desktop/snowball

# Run
./SnowballMain.py 

# Go back.
cd ~

# We are done.
