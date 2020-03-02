#!/usr/bin/python

'''
Setup:
- sudo apt-get update
- sudo apt-get install python-pip libglib2.0-dev
- sudo pip install bluepy
- sudo apt-get install bluetooth
- sudo apt-get install python-bluez

Make Snowball discoverable. 
- sudo hciconfig hci0 piscan

Change the BT Name to Snowball
Update file /etc/machine-info with
PRETTY_HOSTNAME=Snowball

Restart BT service
- service bluetooth restart

############################################
If seening this Error: BluetoothError: (2, 'No such file or directory')
then update the following file: 
- sudo vi /etc/systemd/system/dbus-org.bluez.service
and change the line 

ExecStart=/usr/lib/bluetooth/bluetoothd

to

ExecStart=/usr/lib/bluetooth/bluetoothd --compat

Save then run:
sudo systemctl daemon-reload
sudo systemctl restart bluetooth
sudo chmod 777 /var/run/sdp

Answer Source: https://raspberrypi.stackexchange.com/a/42262
############################################


############################################
If seening this Error: BluetoothError: (13, 'Permission denied')
then your user is likely not in the bluetooth group so add it.
- sudo usermod -G bluetooth -a pi

Create file /etc/systemd/system/var-run-sdp.path with the following content:

[Unit]
Descrption=Monitor /var/run/sdp

[Install]
WantedBy=bluetooth.service

[Path]
PathExists=/var/run/sdp
Unit=var-run-sdp.service

And another file, /etc/systemd/system/var-run-sdp.service:

[Unit]
Description=Set permission of /var/run/sdp

[Install]
RequiredBy=var-run-sdp.path

[Service]
Type=simple
ExecStart=/bin/chgrp bluetooth /var/run/sdp


- sudo systemctl daemon-reload
- sudo systemctl enable var-run-sdp.path
- sudo systemctl enable var-run-sdp.service
- sudo systemctl start var-run-sdp.path
Answer Source: https://stackoverflow.com/questions/34599703/rfcomm-bluetooth-permission-denied-error-raspberry-pi
############################################

'''
import pygame, sys
from pygame.locals import * 

from Snowball import Snowball
from ThrustersBleController import ThrustersBleController
from ThreadBtServer import ThreadBtServer

from SbEventSleep import SbEventSleep
from SbEventHighFive import SbEventHighFive
from SbEventDischarge import SbEventDischarge
from SbEventCharge import SbEventCharge
from SbEventAwaken import SbEventAwaken

class SnowballMain:

	mRunning = True
	
	def __init__(self):
		pass
		
	def run(self):
		
		pygame.init()

		FPS = 30 # Frames per second settings
		mFpsClock = pygame.time.Clock()

		# Hide the mouse cursor
		pygame.mouse.set_visible(False) 

		DISPLAYSURF = pygame.display.set_mode((800, 480), pygame.FULLSCREEN)

		# TODO: Connect To Thrusters BT Device 
		thrusters = ThrustersBleController("E9:DA:27:69:E3:E2")
		thrusters.connect()
		
		# Create Snowball Instance
		mSnowball = Snowball(thrusters, pygame)
		mSnowball.init()

		# Test sleeping state.
		mSnowball.handleEvent(SbEventSleep())
		
		# Spin Client Listening thread so we can connect from the mobile app. 
		btServerThread = ThreadBtServer(self)
		btServerThread.start()
		
		self.mRunning = True 
		while self.mRunning:
			
			# Clear screen by drawing black on it.
			DISPLAYSURF.fill((0,0,0))
			
			for event in pygame.event.get():
				if event.type == QUIT:
					self.mRunning = False
					break
				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						self.mRunning = False 
						break
			
			timeMillis = pygame.time.get_ticks()
		
			if timeMillis > 15000: 
				mSnowball.handleEvent(SbEventAwaken())
		
		
			# Update Snowball
			mSnowball.update(timeMillis)
			
			# Draw Snowball
			mSnowball.draw(DISPLAYSURF)
					
			pygame.display.update()
			mFpsClock.tick(FPS)
		
		thrusters.disconnect()
		btServerThread.stop()	
		pygame.quit()
		sys.exit()

	def shouldRun(self):
		return self.mRunning
		
	'''
	Prepares events to be handled in the next update cycle. 
	'''	
	def queueEvent(self, event):
		# TODO Queue events for handling during the update loop.
		pass
		
if __name__ == '__main__':
	snowbalMain = SnowballMain()
	snowbalMain.run()
	
