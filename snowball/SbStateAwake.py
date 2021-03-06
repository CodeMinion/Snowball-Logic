from FsmState import FsmState
from FsmOwner import FsmOwner

from SbStateTransitioning import SbStateTransitioning

from KeyframeAnimations import *
from pygame.locals import * 

from SbEventDischarge import SbEventDischarge
import SbStatePreDischarge

from SbEventHighFive import SbEventHighFive
import SbStateHighFive

from SbEventSad import SbEventSad
import SbStateSad

from SbEventHappy import SbEventHappy 
import SbStateHappy

from SbEventNineYears import SbEventNineYears
import SbStateNineYears

from SbEventSleep import SbEventSleep
import SbStateFallingAsleep

class SbStateAwake(FsmState):
	
	mAnimation = None
	def __init__(self):
		FsmState.__init__(self)

	'''
	Perform any init steps required for this state.
	'''	
	def onEnter(self, fsmOwner):
		self.mAnimation = fsmOwner.getAnimation("AWAKE")
		self.mAnimation.start()
		fsmOwner.getThrusters().turnOn()
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
		if isinstance(event, SbEventDischarge):
			fsmOwner.getFsm().changeState(SbStatePreDischarge.SbStatePreDischarge())	
		
		elif isinstance(event, SbEventHighFive):
			fsmOwner.getFsm().changeState(SbStateTransitioning(SbStateHighFive.SbStateHighFive()))	
		
		elif isinstance(event, SbEventSad):
			fsmOwner.getFsm().changeState(SbStateSad.SbStateSad())	
		
		elif isinstance(event, SbEventHappy):
			fsmOwner.getFsm().changeState(SbStateHappy.SbStateHappy())	
		
		elif isinstance(event, SbEventNineYears):
			fsmOwner.getFsm().changeState(SbStateTransitioning(SbStateNineYears.SbStateNineYears()))	
		
		elif isinstance(event, SbEventSleep):
			fsmOwner.getFsm().changeState(SbStateFallingAsleep.SbStateFallingAsleep())
		pass
	
	'''
	Handle any clean up here. 
	'''	
	def onExit(self, fsmOwner):
		pass

