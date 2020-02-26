from FsmOwner import FsmOwner
from Fsm import Fsm 
from SbStateInitial import SbStateInitial

class Snowball(FsmOwner):
	
	mSnowballFsm = None
	
	def __init__(self):
		mSnowballFsm = Fsm(self, SbStateInitial())
		FsmOwner.__init__(self, mSnowballFsm)

	def init(self):
		# Do any resource loading needed for Snowball
		pass
		
		
