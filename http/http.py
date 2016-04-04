import socket
import sys
import threading
import os

downloadables = []

class _mainThread (threading.Thread):
	
	def __init__(self, BUFFER_SIZE, io, guiCallback, FILES_PATH):
		threading.Thread.__init__(self)
		self.BUFFER_SIZE = BUFFER_SIZE
		self.io = io
		self.guiCallback = guiCallback
		self.FILES_PATH = FILES_PATH

	def run(self):
		try:
			while 1:
				conn, addr = self.io.accept()
				_connThread(self.BUFFER_SIZE, addr, conn, self.guiCallback, self.FILES_PATH).start()
		finally:
			self.io.close()

class _connThread (threading.Thread):

	def __init__(self, BUFFER_SIZE, addr, conn, guiCallback, FILES_PATH):
		threading.Thread.__init__(self)
		self.BUFFER_SIZE = BUFFER_SIZE
		self.addr = addr
		self.conn = conn
		self.guiCallback = guiCallback
		self.FILES_PATH = FILES_PATH

	def run(self):
		while True:
			req = self.conn.recv(self.BUFFER_SIZE)
			if not req:
				break
			if "GET" in req:
				print "HTTP: GET", req.split("\n")[0].split(" ")[1], "from", self.addr
				fileReq = self.FILES_PATH + req.split("\n")[0].split(" ")[1]
				self._getRequest(fileReq)
				break
			elif "PUT" in req:
				content = req.split("\r\n\r\n")[1]
				print "HTTP: PUT from", self.addr, ":", content
				self._putRequest(content)
				break
			else:
				break

	def _getRequest(self, req):
		self.conn.send('HTTP/1.0 200 OK\r\n')
		try:
			f = open(req, "rb")
			#self.conn.send("Content-Type: image/jpeg\r\n")
			#self.conn.send("Content-Length: "+str(os.path.getsize(req))+"\r\n")
			#self.conn.send("Connection: keep-alive\r\n")
			self.conn.send("\r\n")
			line = f.read(self.BUFFER_SIZE)
			print "HTTP: Sending", req
			while line:
				self.conn.send(line)
				line = f.read(self.BUFFER_SIZE)
			f.close()
		except:
			print "HTTP: Not found!", req
		self.conn.close()

	def _putRequest(self, content):
		if content not in downloadables:
			downloadables.append(content)
			print "HTTP: New downloadable: " + content
			downloadable = str(self.addr[0]) + " : " + content
			self.guiCallback(downloadable)
		self.conn.send('HTTP/1.0 200 OK\r\n')
		self.conn.close()
 
class HTTP:

	def __init__(self, TCP_PORT, guiCallback, FILES_PATH):
		self.TCP_IP = str(self._getMyIP)
		self.BUFFER_SIZE = 1024
		self.guiCallback = guiCallback
		self.FILES_PATH = FILES_PATH
		if TCP_PORT is not None:
			self.TCP_PORT = TCP_PORT
		else:
			self.TCP_PORT = 8080

	def start(self):
		# Create TCP Socket
		try:
			io = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			io.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			io.bind(('', self.TCP_PORT))
			io.listen(1)
			print "HTTP: Server starting..."
			print "HTTP: Server listening port ", self.TCP_PORT, "..."
		except socket.error, msg:
			print "HTTP: Failed to create socket. Error code: "+str(msg[0])+", Error message : "+str(msg[1])
			sys.exit()
		# Listen to HTTP requests
		_mainThread(self.BUFFER_SIZE, io, self.guiCallback, self.FILES_PATH).start()

	def sendFile(self, addr, fileName):
		print "sending:", fileName, "to:", addr

	def downloadFile(self, item):
		print "Downloading: ", item.split(":",1)[1].strip(), " from: ", item.split(":",1)[0].strip()
		#document = "/"
		""" "%s %s HTTP/1.0"  % (command, document or /) """

	def _getMyIP():
		cmd = "ifconfig wlan0| grep 'inet addr' | cut -d: -f2 | awk '{ print $1}'"
		return subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE).communicate()[0]
		
