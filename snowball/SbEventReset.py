from FsmEvent import FsmEvent

'''
Event to signal Snowball to go to go back to the initial state.
'''
class SbEventReset (FsmEvent):
	
	def __init__(self):
		pass
