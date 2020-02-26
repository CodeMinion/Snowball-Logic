class FsmOwner: 
	
	mFsm = None
	
	def __init__(self, fsm):
		mFsm = fsm

	'''
	Get a reference to the Finite State Machine of this owner.
	'''
	def getFsm():
		return mFsm
	
	'''
	Perform an update of this owner entity. 
	'''	
	def update(self, timeMillis):
		mFsm.onUpdate(self, timeMillis)
	
	'''
	Handle events. 
	'''	
	def handleEvent(self, event):
		mFsm.onEvent(self, event)

	'''
	Perform any draw. 
	'''
	def draw(self, drawSurface):
		mFsm.onDraw(self, drawSurface)
