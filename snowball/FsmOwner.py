class FsmOwner: 
	
	mFsm = None
	
	def __init__(self, fsm):
		self.mFsm = fsm

	'''
	Get a reference to the Finite State Machine of this owner.
	'''
	def getFsm():
		return self.mFsm
	
	'''
	Perform an update of this owner entity. 
	'''	
	def update(self, timeMillis):
		self.mFsm.onUpdate(timeMillis)
	
	'''
	Handle events. 
	'''	
	def handleEvent(self, event):
		self.mFsm.onEvent(event)

	'''
	Perform any draw. 
	'''
	def draw(self, drawSurface):
		self.mFsm.onDraw(drawSurface)
