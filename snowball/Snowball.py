from FsmOwner import FsmOwner
from Fsm import Fsm 
from SbStateInitial import SbStateInitial

class Snowball(FsmOwner):
	
	def __init__(self):
		snowballFsm = Fsm(self, SbStateInitial())
		FsmOwner.__init__(self, snowballFsm)

	def init(self):
		# Do any resource loading needed for Snowball
		pass
		

		
		
