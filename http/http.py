import socket
import sys
import threading

downloadables = []

class _mainThread (threading.Thread):
	
	def __init__(self, TCP_IP, TCP_PORT, BUFFER_SIZE, io, guiCallback):
		threading.Thread.__init__(self)
		self.TCP_IP = TCP_IP
		self.TCP_PORT  = TCP_PORT
		self.BUFFER_SIZE = BUFFER_SIZE
		self.io = io
		self.guiCallback = guiCallback

	def run(self):
		try:
			while 1:
				conn, addr = self.io.accept()
				_connThread(self.TCP_IP, self.TCP_PORT, self.BUFFER_SIZE, addr, conn, self.guiCallback).start()
		finally:
			self.io.close()

class _connThread (threading.Thread):

	def __init__(self, TCP_IP, TCP_PORT, BUFFER_SIZE, addr, conn, guiCallback):
		threading.Thread.__init__(self)
		self.TCP_IP = TCP_IP
		self.TCP_PORT  = TCP_PORT
		self.BUFFER_SIZE = BUFFER_SIZE
		self.addr = addr
		self.conn = conn
		self.guiCallback = guiCallback

	def run(self):
		req = ""
		while True:
			data = self.conn.recv(self.BUFFER_SIZE)
			if not data:
				break
			req = req + data
			if "GET" in req:
				print "HTTP: GET from ", self.addr
				_getRequest(self.conn)
				break
			elif "PUT" in req:
				content = req.split("\r\n\r\n")[1]
				print "HTTP: PUT from ", self.addr, " : ", content
				_putRequest(self.conn, self.addr, content, self.guiCallback)
				break
			else:
				break

def _getRequest(conn):
	conn.send('HTTP/1.0 200 OK\r\n')
	conn.send("Content-Type: text/html\r\n\r\n")
	conn.send('<html><body><h1>Hello World</body></html>')
	conn.close()

def _putRequest(conn, addr, content, guiCallback):
	if content not in downloadables:
		downloadables.append(content)
		print "HTTP: New downloadable: " + content
		downloadable = str(addr[0]) + " : " + content
		guiCallback(downloadable)
	print "HTTP: Maby respond put ok?"
	conn.close()
 
class HTTP:

	def __init__(self, TCP_PORT, guiCallback):
		self.TCP_IP = '127.0.0.1'
		self.BUFFER_SIZE = 1024
		self.guiCallback = guiCallback
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
			print "HTTP: Server starting..."
			print "HTTP: Server listening port ", self.TCP_PORT, "..."
		except socket.error, msg:
			print "HTTP: Failed to create socket. Error code: "+str(msg[0])+", Error message : "+str(msg[1])
			sys.exit()
		# Listen to HTTP requests
		_mainThread(self.TCP_IP, self.TCP_PORT, self.BUFFER_SIZE, io, self.guiCallback).start()

	def sendFile(self, addr, fileName):
		print "sending: ", fileName, " to: ", addr

	def downloadFile(self, item):
		print "Downloading: ", item.split(":",1)[1].strip(), " from: ", item.split(":",1)[0].strip()
		#document = "/"
		""" "%s %s HTTP/1.0"  % (command, document or /) """
		
