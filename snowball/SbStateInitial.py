from FsmState import FsmState
from FsmOwner import FsmOwner

from FsmEvent import FsmEvent

from SbEventSleep import SbEventSleep
from SbStateSleeping import SbStateSleeping

from SbEventHighFive import SbEventHighFive
from SbStateHighFive import SbStateHighFive

from SbEventDischarge import SbEventDischarge
from SbStateDischarging import SbStateDischarging

from SbStateTransitioning import SbStateTransitioning

from SbEventCharge import SbEventCharge
from SbStateCharging import SbStateCharging

class SbStateInitial(FsmState):
	
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
		if isinstance(event, SbEventSleep):
			fsmOwner.getFsm().changeState(SbStateSleeping())
			
		elif isinstance(event, SbEventHighFive):
			fsmOwner.getFsm().changeState(SbStateHighFive())
			
		elif isinstance(event, SbEventDischarge):
			fsmOwner.getFsm().changeState(SbStateDischarging())
			
		elif isinstance(event, SbEventCharge):
			fsmOwner.getFsm().changeState(SbStateTransitioning(SbStateCharging()))
		pass
	
	'''
	Handle any clean up here. 
	'''	
	def onExit(self, fsmOwner):
		pass

