from FsmState import FsmState
from FsmOwner import FsmOwner

from KeyframeAnimations import *
from pygame.locals import * 

from SbEventCharge import SbEventCharge
import SbStateCharging
import SbStateTransitioning

class SbStateDischarged(FsmState):
	
	def __init__(self):
		FsmState.__init__(self)
	
	'''
	Perform any init steps required for this state.
	'''	
	def onEnter(self, fsmOwner):
		pass
		
	'''
	Perform any logic needed on the update state.
	'''
	def onUpdate(self, fsmOwner, timeMilis):
		pass
		
	'''
	Perform any drawing here.
	'''	
	def onDraw(self, fsmOwner, drawSurface):
		pass
	
	'''
	Handle any events here.
	'''	
	def onEvent(self, fsmOwner, event):
	
		if isinstance(event, SbEventCharge):
			# Move to charging state.
			fsmOwner.getFsm().changeState(SbStateTransitioning.SbStateTransitioning(SbStateCharging.SbStateCharging()))
		pass
	
	'''
	Handle any clean up here. 
	'''	
	def onExit(self, fsmOwner):
		pass

