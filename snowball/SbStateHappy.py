from FsmState import FsmState
from FsmOwner import FsmOwner

import SbStateAwake
from SbStateTransitioning import SbStateTransitioning
from SbEventReset import SbEventReset

from KeyframeAnimations import *
from pygame.locals import * 

class SbStateHappy(FsmState):
	
	mAnimation = None
	def __init__(self):
		FsmState.__init__(self)

	'''
	Perform any init steps required for this state.
	'''	
	def onEnter(self, fsmOwner):
		self.mAnimation = fsmOwner.getAnimation("HAPPY")
		self.mAnimation.start()
		pass
		
	'''
	Perform any logic needed on the update state.
	'''
	def onUpdate(self, fsmOwner, timeMilis):
		self.mAnimation.update(timeMilis)
		pass
		
	'''
	Perform any drawing here.
	'''	
	def onDraw(self, fsmOwner, drawSurface):
		currKeyframe = self.mAnimation.getCurrentFrame()
		keyframeSource = currKeyframe.getSource()
		sourceRect = Rect((keyframeSource[0], keyframeSource[1]), (keyframeSource[2],keyframeSource[3]))
		dest = (0,0)
		drawSurface.blit(self.mAnimation.getSpriteSheet(), dest, sourceRect)
		
		pass
	
	'''
	Handle any events here.
	'''	
	def onEvent(self, fsmOwner, event):
		# Go to the back to idle State.
		if isinstance(event, SbEventReset):
			fsmOwner.getFsm().changeState(SbStateTransitioning(SbStateAwake.SbStateAwake()))
		pass
	
	'''
	Handle any clean up here. 
	'''	
	def onExit(self, fsmOwner):
		pass

