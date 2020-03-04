import bluetooth
import threading
import struct

from SbEventSleep import SbEventSleep
from SbEventHighFive import SbEventHighFive
from SbEventDischarge import SbEventDischarge
from SbEventCharge import SbEventCharge
from SbEventAwaken import SbEventAwaken
from SbEventReset import SbEventReset

class ThreadBtClient(threading.Thread):

	# Reference to the Snowball Controller
	mSnowballController = None
	
	# Reference to client socket
	mClient = None

	# Continue running?
	mRunning = True

	def __init__(self, clientSocket, snowballController):
		threading.Thread.__init__(self)
		self.mSnowballController = snowballController
		self.mClient = clientSocket

	# Receive data as long as the socket is active.
	def run(self):
		try:
			while self.mRunning:
			
				msgSizeBytes = self.mClient.recv(4)
				msgSize = struct.unpack('<i', msgSizeBytes)[0]
				chunks = []
				bytes_received = 0
				while bytes_received < msgSize:
					chunk = self.mClient.recv(min(msgSize - bytes_received, 1024))
					bytes_received = bytes_received + len(chunk)
					if chunk == b'':
						#TODO  Handle Network Error
						pass
					chunks.append(chunk)
							
				data = b''.join(chunks)#self.client.recv(1024)
				command = '{0}'.format(data)
				#print 'Command Received {0}'.format(command)
				# TODO Interpret command into event. 
				event = self.translateEvent(command)
				#print 'Event Translated {0}'.format(event)
				if event is not None:
					self.mSnowballController.queueEvent(event)	
				
		except IOError as e:
			print '{0}'.format(e)
			pass
	
	# Send data back to the client. 	
	def send(self, data):
		try:
			totalSent = 0
			msgLen = len(data)
			dataToSend = struct.pack('<i', msgLen) + data
			toSendLen = len(dataToSend)
			while totalSent < toSendLen:
				sent = self.mClient.send(dataToSend[totalSent:])
				if sent == 0:
					#TODO Handle Network Error
					pass
				totalSent = totalSent + sent
				
		except IOError as e:
			pass

	# Close the connections
	def close(self):
		try:
			self.mClient.close()
			self.mRunning = False
		
		except IOError as e:
			pass

	def translateEvent(self, eventStr):
		event = None
		
		if eventStr == 'SLEEP':
			event = SbEventSleep()
		elif eventStr == 'WAKE_UP':
			event = SbEventAwaken()
		elif eventStr == 'DISCHARGE':
			event = SbEventDischarge()
		elif eventStr == 'RECHARGE':
			event = SbEventCharge()
		elif eventStr == 'HIGH_FIVE':
			event = SbEventHighFive()
		elif eventStr == 'HAPPY':
			event = None
		elif eventStr == 'SAD':
			event = None
		elif eventStr == 'RESET':
			event = SbEventReset()
								
		return event
		pass
