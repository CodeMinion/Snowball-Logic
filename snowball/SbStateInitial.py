from FsmState import FsmState
from FsmOwner import FsmOwner

from FsmEvent import FsmEvent

from SbStateTransitioning import SbStateTransitioning

from SbEventCharge import SbEventCharge
from SbStateCharging import SbStateCharging

from SbEventDischarge import SbEventDischarge
from SbStateDischarging import SbStateDischarging

from SbEventHighFive import SbEventHighFive
import SbStateHighFive

from SbEventSad import SbEventSad
import SbStateSad

from SbEventHappy import SbEventHappy 
import SbStateHappy

from SbEventNineYears import SbEventNineYears
import SbStateNineYears

from SbEventSleep import SbEventSleep
import SbStateSleeping


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
			fsmOwner.getFsm().changeState(SbStateSleeping.SbStateSleeping())
			
		elif isinstance(event, SbEventHighFive):
			fsmOwner.getFsm().changeState(SbStateHighFive.SbStateHighFive())
			
		elif isinstance(event, SbEventDischarge):
			fsmOwner.getFsm().changeState(SbStateDischarging())
			
		elif isinstance(event, SbEventCharge):
			fsmOwner.getFsm().changeState(SbStateTransitioning(SbStateCharging()))
			
		elif isinstance(event, SbEventSad):
			fsmOwner.getFsm().changeState(SbStateTransitioning(SbStateSad.SbStateSad()))
			
		elif isinstance(event, SbEventHappy):
			fsmOwner.getFsm().changeState(SbStateTransitioning(SbStateHappy.SbStateHappy()))
			
		pass
	
	'''
	Handle any clean up here. 
	'''	
	def onExit(self, fsmOwner):
		pass

