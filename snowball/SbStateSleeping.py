from FsmState import FsmState
from FsmOwner import FsmOwner

from KeyframeAnimations import *
from pygame.locals import * 

class SbStateSleeping(FsmState):
	
	mSleepingAnimation = None
	def __init__(self):
		FsmState.__init__(self)

	'''
	Perform any init steps required for this state.
	'''	
	def onEnter(self, fsmOwner):
		self.mSleepingAnimation = fsmOwner.getAnimation("SLEEPING")
		pass
		
	'''
	Perform any logic needed on the update state.
	'''
	def onUpdate(self, fsmOwner, timeMilis):
		self.mSleepingAnimation.update(timeMilis)
		pass
		
	'''
	Perform any drawing here.
	'''	
	def onDraw(self, fsmOwner, drawSurface):
		currKeyframe = self.mSleepingAnimation.getCurrentFrame()
		keyframeSource = currKeyframe.getSource()
		sourceRect = Rect((keyframeSource[0], keyframeSource[1]), (keyframeSource[2],keyframeSource[3]))
		# In the case of the sleeping animation the source and 
		# destination are the same size so we can use the same coordinates 
		dest = (keyframeSource[0], keyframeSource[1])
		drawSurface.blit(self.mSleepingAnimation.getSpriteSheet(), dest, sourceRect)
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

