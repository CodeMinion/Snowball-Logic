#!/usr/bin/python

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
		
		mRunning = True 
		while mRunning:
			
			# Clear screen by drawing black on it.
			DISPLAYSURF.fill((0,0,0))
			
			for event in pygame.event.get():
				if event.type == QUIT:
					mRunning = False
					break
				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						mRunning = False 
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
	
