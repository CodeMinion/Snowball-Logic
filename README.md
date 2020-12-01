# Snowball Logic
This is the code that runs the Snowball Prop and is controlled over Blutooth using the Android applications found here: 


## Installing the code
 Install desktop Raspberry Pi image.

### Update:
 ```
sudo apt-get update
sudo apt-get install python-pip libglib2.0-dev
sudo pip install bluepy
sudo apt-get install bluetooth
sudo apt-get install python-bluez
```

### Copy logic code:
Copy the files in this repo to your Raspberry Pi. For the remaining of these instructions they will assume it has been copied to the location: **/home/pi/Desktop/snowball/**

### Configure to run at boot time:
Copy SnowballBoot.sh to the /boot dir
```
cp SnowballBoot.sh /boot/
cd /boot
```
Make exucutable 
```
 chmod 755 SnowballBoot.sh
```

Add to crontb 
```
sudo contrab -e
@reboot sh sudo sh /boot/SnowballBoot.sh > /home/pi/Desktop/snowball/cronlogs 2>&1
```


Make Snowball discoverable. 
```
sudo hciconfig hci0 piscan
```    
Change the BT Name to Snowball
```
# Update file /etc/machine-info with
PRETTY_HOSTNAME=Snowball
```
 
## Errors:
During the first execution the following errors may or may not occur. Below are the two most common errors and how to address them. 

### Error: BluetoothError: (2, 'No such file or directory') 
If seeing Error: **BluetoothError: (2, 'No such file or directory')** then update the following file:

```
sudo vi /etc/systemd/system/dbus-org.bluez.service
# and change the line
ExecStart=/usr/lib/bluetooth/bluetoothd
# to 
ExecStart=/usr/lib/bluetooth/bluetoothd --compat
```
Save then run:
```
sudo systemctl daemon-reload
sudo systemctl restart bluetooth
sudo chmod 777 /var/run/sdp
```

**Source:** Source: https://raspberrypi.stackexchange.com/a/42262


### Error: BluetoothError: (13, 'Permission denied')
If seening this **Error: BluetoothError: (13, 'Permission denied')** then your user is likely not in the bluetooth group so add it.
```
sudo usermod -G bluetooth -a pi
```
Create file /etc/systemd/system/var-run-sdp.path with the following content:
```
[Unit]
Descrption=Monitor /var/run/sdp

[Install]
WantedBy=bluetooth.service

[Path]
PathExists=/var/run/sdp
Unit=var-run-sdp.service
```
And another file, /etc/systemd/system/var-run-sdp.service:
```
[Unit]
Description=Set permission of /var/run/sdp

[Install]
RequiredBy=var-run-sdp.path

[Service]
Type=simple
ExecStart=/bin/chgrp bluetooth /var/run/sdp
```

Then execute: 
```
sudo systemctl daemon-reload
sudo systemctl enable var-run-sdp.path
sudo systemctl enable var-run-sdp.service
sudo systemctl start var-run-sdp.path
```
Source: https://stackoverflow.com/questions/34599703/rfcomm-bluetooth-permission-denied-error-raspberry-pi


# Thrusters LED Nrf52
Sketch for the Feather Nrf52 from Adafruit to derive the LEDs in the thrusters of Snowball. The sketch expects the LEDs to be wired to pin A7 on the Feather. Once Snowball boots it will handle the connection to the feather as well as turning the thrusters On/Off. Once flashed update the thrusters line in SnowballMain.py with your Feather's address.
```
# BT Address of the Feather Nrf52
ThrustersBleController("E9:DA:27:69:E3:E2")
```

License
----

**Snowball Logic** is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. **Snowball Logic** is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the [GNU Lesser General Public License](https://www.gnu.org/licenses/lgpl-3.0.en.html) for more details. You should have received a copy of the GNU Lesser General Public License along with **Snowball Logic**. If not, see [this](https://www.gnu.org/licenses/lgpl-3.0.en.html)





