from multicast import multicast
from http import http
from gui import gui
import threading
import sys, os

MCAST_GROUP = "224.0.0.251"
MCAST_PORT  = 3003
HTTP_PORT   = 8081
BASE_PATH   = os.path.dirname(os.path.realpath(__file__))

# Create User Interface object
gui = gui.GUI(MCAST_GROUP, MCAST_PORT, BASE_PATH)
# Create http server and inject gui
http = http.HTTP(HTTP_PORT, gui.newDownloadable)
http.start()
# Create multicast socket and inject gui
multicast.start(MCAST_GROUP, MCAST_PORT, gui.newUser)
# Set gui http functions
gui.setSendFunction(http.sendFile)
gui.setDownloadFunction(http.downloadFile)
# Start gui
gui.start()

# Exit everything, including all threads
os._exit(1)