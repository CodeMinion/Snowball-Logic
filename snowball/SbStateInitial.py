from FsmState import FsmState
from FsmOwner import FsmOwner

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
		pass
	
	'''
	Handle any clean up here. 
	'''	
	def onExit(self, fsmOwner):
		pass

