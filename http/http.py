import socket
import sys
import threading

class _mainThread (threading.Thread):
	
	def __init__(self, TCP_IP, TCP_PORT, BUFFER_SIZE, io, gui):
		threading.Thread.__init__(self)
		self.TCP_IP = TCP_IP
		self.TCP_PORT  = TCP_PORT
		self.BUFFER_SIZE = BUFFER_SIZE
		self.io = io
		self.gui = gui

	def run(self):
		try:
			while 1:
				conn, addr = self.io.accept()
				print "Connected with: ", addr[0], ":", addr[1]
				_connThread(self.TCP_IP, self.TCP_PORT, self.BUFFER_SIZE, conn).start()
		finally:
			self.io.close()

class _connThread (threading.Thread):

	def __init__(self, TCP_IP, TCP_PORT, BUFFER_SIZE, conn):
		threading.Thread.__init__(self)
		self.TCP_IP = TCP_IP
		self.TCP_PORT  = TCP_PORT
		self.BUFFER_SIZE = BUFFER_SIZE
		self.conn = conn

	def run(self):

		self.conn.send('HTTP/1.0 200 OK\r\n')
		self.conn.send("Content-Type: text/html\r\n\r\n")
		self.conn.send('<html><body><h1>Hello World</body></html>')
		self.conn.close()

		#self.conn.send("Welcome!\n")
		"""
		while True:
			data = self.conn.recv(self.BUFFER_SIZE)
			reply = "OK!...\n"+data
			if not data:
				break
			self.conn.send(data)
		self.conn.close()
		"""
 
class HTTP:

	def __init__(self, TCP_PORT, gui):
		self.TCP_IP = '127.0.0.1'
		self.BUFFER_SIZE = 1024
		self.gui = gui
		if TCP_PORT is not None:
			self.TCP_PORT = TCP_PORT
		else:
			self.TCP_PORT = 8080

	def start(self):
		# Create TCP Socket
		try:
			io = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			io.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			io.bind((self.TCP_IP, self.TCP_PORT))
			io.listen(1)
			print "HTTP server starting..."
			print "HTTP server listening port ", self.TCP_PORT, "..."
		except socket.error, msg:
			print "Failed to create HTTP Server socket. Error code: "+str(msg[0])+", Error message : "+str(msg[1])
			sys.exit()
		# Listen to HTTP requests
		_mainThread(self.TCP_IP, self.TCP_PORT, self.BUFFER_SIZE, io, self.gui).start()
		
