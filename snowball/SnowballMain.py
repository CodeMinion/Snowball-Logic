#!/usr/bin/python

import pygame, sys
from pygame.locals import * 

from Snowball import Snowball

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
		# TODO: Sping Client Listening thread so we can connect from the mobile app. 

		# TODO: Create Snowball Instance
		mSnowball = Snowball()
		mSnowball.init()

		mRunning = True 
		while mRunning:
			for event in pygame.event.get():
				if event.type == QUIT:
					mRunning = False
					break
				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						mRunning = False 
						break
			
			# TODO Update Snowball
						
			pygame.display.update()
			mFpsClock.tick(FPS)
			
		pygame.quit()
		sys.exit()

if __name__ == '__main__':
	snowbalMain = SnowballMain()
	snowbalMain.run()
	
