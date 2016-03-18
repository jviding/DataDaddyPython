from multicast import multicast
from http import http
from gui import gui
import threading
import sys, os

MCAST_GROUP = "224.0.0.251"
MCAST_PORT  = 3003
HTTP_PORT   = 8080

# Create User Interface object
gui = gui.GUI(MCAST_GROUP, MCAST_PORT)
# Create http server and inject gui
#http = http.HTTP(HTTP_PORT, gui)
#http.start()
# Create multicast socket and inject gui
multicast.start(MCAST_GROUP, MCAST_PORT, gui)
# Start gui
gui.start()

# Exit everything, including all threads
os._exit(1)