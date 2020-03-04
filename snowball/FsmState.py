from SbStateInitial import SbStateInitial

class FsmState:
	
	def __init__(self):
		pass
		
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
		if isinstance(event, SbEventReset):
			fsmOwner.getFsm().changeState(SbStateTransitioning(SbStateInitial()))
		
		pass
	
	'''
	Handle any clean up here. 
	'''	
	def onExit(self, fsmOwner):
		pass
