import threading
import bluetooth
import time

class ThreadBtServer(threading.Thread):

	#Instance of the main controller so we can forward events it. 
	mSnowballMain = None
	
	# Bluetooth Servie Name
	mBtName = 'Snowball Controller'
	# Snowball Controller UUID
	mBtUuid = '385a5cd2-d573-11e4-b9d6-1681e6b88ec1'
	
	mBtServerSocket = None
	
	
	# Set if we want to listen on a given BT interface, leave blank for auto select.
	# Useful in device where we have more than one BT adapter.
	mServerInterfaceMac = ''
	
	def __init__(self, snowballMain):
		threading.Thread.__init__(self)
		self.mSnowballMain = snowballMain
		pass
		
	def run(self):
		
		self.mBtServerSocket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		port = 29#bluetooth.PORT_ANY
		
		res = self.mBtServerSocket.bind((self.mServerInterfaceMac, port))
		
		self.mBtServerSocket.listen(1)
		port = self.mBtServerSocket.getsockname()[1]
		#time.sleep(5)
		print 'Listening on Port: {0}'.format(port)

		# Advertise service
		bluetooth.advertise_service(self.mBtServerSocket, self.mBtName, self.mBtUuid)
		#time.sleep(2)
		while self.shouldRun():
			try:

				print 'Waiting for Clients...'
				client_sock, client_addr = self.mBtServerSocket.accept()
				print '{0}: Connection Accepted'.format(client_addr)
				
				# TODO Spin Client Thread. 
				snowballClient = ThreadBtClient(client_sock, self.mSnowballMain)
				snowballClient.setDaemon(True)
				snowballClient.start()
				
			except KeyboardInterrupt as key:
				bluetooth.stop_advertising(self.btServerSocket)
				break
		pass