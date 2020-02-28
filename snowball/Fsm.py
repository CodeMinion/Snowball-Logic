from FsmState import FsmState
from FsmOwner import FsmOwner

class Fsm:
	
	mPrevState = None
	mCurrState = None
	mFsmOwner = None 
	
	def __init__(self, owner, startState):
		self.mFsmOwner = owner
		self.changeState(startState)
		pass
	
	'''
	Move the Finite state machine to the next state.
	'''
	def changeState(self, nextState):
		if self.mCurrState is not None:
			self.mCurrState.onExit(self.mFsmOwner)
			
		# Track previous state in case we want to support revert.	
		self.mPrevState = self.mCurrState
		
		self.mCurrState = nextState
		
		if self.mCurrState is not None:
			self.mCurrState.onEnter(self.mFsmOwner)

	'''
	Handle update calls.
	'''	
	def onUpdate(self, timeMillis):
		if self.mCurrState is not None:
			self.mCurrState.onUpdate(self.mFsmOwner, timeMillis)
	
	'''
	Handle draw calls.
	'''
	def onDraw(self, drawSurface):
		if self.mCurrState is not None: 
			self.mCurrState.onDraw(self.mFsmOwner, drawSurface)
	
	'''
	Handle events. 
	'''		
	def onEvent(self, event):
		if self.mCurrState is not None:
			self.mCurrState.onEvent(self.mFsmOwner, event)
