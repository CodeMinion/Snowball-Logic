from bluepy.btle import *
from struct import *
import threading

class ThrustersBleController(DefaultDelegate):
	
	# MAC of the thrusters device. 
	mThrustersMac = None
	
	mTrustersPeripheral = None
	
	# Thrusters BLE Details
	mThrustersServiceUuid = "000038FF-0000-1000-8000-00805F9B34FB"
	mThrustersCharacteristicUuid = "00003A38-0000-1000-8000-00805F9B34FB"
	
	mThrustersService = None
	mThrustersCharacteristic = None
	
	def __init__(self, thrustersMac):
		DefaultDelegate.__init__(self)
		self.mThrustersMac = thrustersMac
		pass
	
	'''
	Attempt to connect to the thrusters. 
	'''
	def connect(self):
		try:
			# Connect to the motion sensor using hci1 interface (Note: Consider changing this to be better controlled)
			# 0 - /dev/hci0
			# 1 - /dev/hci1
			self.mTrustersPeripheral = Peripheral(self.mThrustersMac, ADDR_TYPE_RANDOM , 0)
				
			self.mTrustersPeripheral.setDelegate(self)
				
			self.mThrustersService = self.mTrustersPeripheral.getServiceByUUID(self.mThrustersServiceUuid)
			self.mThrustersCharacteristic = self.mThrustersService.getCharacteristics(self.mThrustersCharacteristicUuid)[0]
	
			print 'Connection to Thrusters: {0} - SUCCESS'.format(self.mThrustersMac)
				
		except BTLEException as btErr:
			print 'Connection to Thrusters: {0} - FAILED'.format(self.mThrustersMac)
			print 'Exception {0}'.format(btErr)
			return -1
			
			
		pass
		
	'''
	Turns the thrusters on. 
	'''	
	def turnOn(self):
		onData = struct.pack('<b', 0x01)
		#print 'Turning Thrusters On'
		self.mThrustersCharacteristic.write(onData)
		pass
	
	'''
	Turns the thrusters off.
	'''	
	def turnOff(self):
		offData = struct.pack('<b', 0x00)
		#print 'Turning Thrusters Off'
		self.mThrustersCharacteristic.write(offData)
		pass
	
	# Attempts to disconnect from the 
	# device.
	def disconnect(self):
		if(self.mTrustersPeripheral is not None):
			self.mTrustersPeripheral.disconnect()
			self.mTrustersPeripheral = None
		pass
			
