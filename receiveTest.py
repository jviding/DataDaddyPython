import socket
import struct
import sys

multicast_group = '224.0.0.251'
server_address = ('', 3003)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind to the server address
sock.bind(server_address)

# Tell the operating system to add the socket to the multicast group
# on all interfaces.
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Receive/respond loop
while True:
    print >>sys.stderr, '\nwaiting to receive message'
    data = bytearray(1)
    nbytes, address = sock.recvfrom_into(data, 1)
    print "received actually", nbytes, " bytes"
    print >>sys.stderr, 'received %s bytes from %s' % (len(data), address)
    print >>sys.stderr, data
    print (data[0] & 1)

    #print >>sys.stderr, 'sending acknowledgement to', address
    #sock.sendto('ack', address)