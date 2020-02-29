from FsmState import FsmState
from FsmOwner import FsmOwner

from KeyframeAnimations import *
from pygame.locals import * 

class SbStateTransitioning(FsmState):
	
	mAnimation = None
	mNextState = None
	def __init__(self, nextState):
		FsmState.__init__(self)
		self.mNextState = nextState

	'''
	Perform any init steps required for this state.
	'''	
	def onEnter(self, fsmOwner):
		self.mAnimation = fsmOwner.getAnimation("TRANSITION")
		self.mAnimation.start()
		
		pass
		
	'''
	Perform any logic needed on the update state.
	'''
	def onUpdate(self, fsmOwner, timeMillis):
		self.mAnimation.update(timeMillis)
		
		pass
		
	'''
	Perform any drawing here.
	'''	
	def onDraw(self, fsmOwner, drawSurface):
		currKeyframe = self.mAnimation.getCurrentFrame()
		
		keyframeSource = currKeyframe.getSource()
		sourceRect = Rect((keyframeSource[0], keyframeSource[1]), (keyframeSource[2],keyframeSource[3]))
		dest = (0, 0)
		drawSurface.blit(self.mAnimation.getSpriteSheet(), dest, sourceRect)
		
		# If the transition animation is done, move to the next state.
		if self.mAnimation.isFinished(): 
			fsmOwner.getFsm().changeState(self.mNextState)
		
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

