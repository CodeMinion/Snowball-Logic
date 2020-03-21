from FsmState import FsmState
from FsmOwner import FsmOwner

import SbStateTransitioning
import SbStateDischarging

from KeyframeAnimations import *
from pygame.locals import * 


class SbStatePreDischarge(FsmState):
	
	mAnimation = None
	def __init__(self):
		FsmState.__init__(self)

	'''
	Perform any init steps required for this state.
	'''	
	def onEnter(self, fsmOwner):
		self.mAnimation = fsmOwner.getAnimation("FALLING-ASLEEP")
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
		
		# Go to the discharged State.
		if self.mAnimation.isFinished():
			fsmOwner.getFsm().changeState(SbStateTransitioning.SbStateTransitioning(SbStateDischarging.SbStateDischarging()))
			pass
		
		pass
	
	'''
	Handle any events here.
	'''	
	def onEvent(self, fsmOwner, event):
		pass
	
	'''
	Handle any clean up here. 
	'''	
	def onExit(self, fsmOwner):
		pass

