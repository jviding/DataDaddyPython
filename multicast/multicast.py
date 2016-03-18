import socket
import struct
import threading
import subprocess
import time

devices = []

# THREAD

class _mCastThread (threading.Thread):

	def __init__(self, gui, io, myIP):
		threading.Thread.__init__(self)
		self.gui = gui
		self.io = io
		self.myIP = myIP

	def run(self):
		while True:
			data = bytearray(1)
			nbytes, address = self.io.recvfrom_into(data, 1)
			if (self.myIP.strip() != address[0].strip()):
				if (data[0] == 1):
					newDevice(address[0], self.gui)
					self.io.sendto(bytearray(1), address)
				else:
					newDevice(address[0], self.gui)

# FUNCTIONS

def newDevice(device, gui):
	if device not in devices:
		devices.append(device)
		print "New device found: " + str(device)
		gui.newUser(device)

def _getMyIP():
	cmd = "ifconfig wlan0| grep 'inet addr' | cut -d: -f2 | awk '{ print $1}'"
	return subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE).communicate()[0]

def _createUdpPackageForJoin(MCAST_PORT):
	# UDP package data
	joinMsg = bytearray(1)
	joinMsg[0] = 1
	# UDP package headers
	source_port = MCAST_PORT    # Spoof source for wanted response port
	dest_port = MCAST_PORT      # Send to multicast group
	length = 8+len(joinMsg)     # Package size in bytes
	checksum = 0                # kernel will add this
	# Build UDP header block
	udp_header_bits = bytearray(8)
	struct.pack_into('!4H', udp_header_bits, 0, source_port, dest_port, length, checksum)
	return udp_header_bits+joinMsg

def _joinMulticastGroup(MCAST_GROUP, MCAST_PORT):
	# Use a raw UDP package for multicasting
	io = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
	#io = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	io.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	# Set time to live
	ttl = struct.pack('b', 1)
	io.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
	# Send package
	package = _createUdpPackageForJoin(MCAST_PORT)
	io.sendto(package, (MCAST_GROUP, MCAST_PORT))
	io.close()

def _createMulticastSocket(MCAST_GROUP, MCAST_PORT):
	# Create socket for MultiCast communication
	io = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	# Enable MultiCast communication by setting flag
	io.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	# Bind the socket to the port
	io.bind(('', MCAST_PORT))
	# Tell the OS to add the socket to the multicast group on all interfaces
	mreq = struct.pack('4sL', socket.inet_aton(MCAST_GROUP), socket.INADDR_ANY)
	io.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
	# Set time to live for packages
	ttl = struct.pack('b', 1)
	io.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
	return io

def start(MCAST_GROUP, MCAST_PORT, gui):
	print "Starting multicast..."
	# Create Multicast UDP Socket
	io = _createMulticastSocket(MCAST_GROUP, MCAST_PORT)
	# Get own IP address for filtering own packages from Multicast
	myIP = _getMyIP()
	# Start listening to a multicast socket. Set process to its own thread.
	_mCastThread(gui, io, myIP).start()
	print "Multicasting in group ", MCAST_GROUP, ", port ", MCAST_PORT
	# Join multicast group
	_joinMulticastGroup(MCAST_GROUP, MCAST_PORT)

def rejoin(MCAST_GROUP, MCAST_PORT):
	_joinMulticastGroup(MCAST_GROUP, MCAST_PORT)