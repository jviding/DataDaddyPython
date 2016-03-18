from Tkinter import *
from multicast import multicast

class GUI():

	def __init__(self, MCAST_GROUP, MCAST_PORT):
		self.MCAST_GROUP = MCAST_GROUP
		self.MCAST_PORT  = MCAST_PORT
		# MAIN WINDOW
		mainWindow = PanedWindow(orient=VERTICAL)
		mainWindow.pack(fill=BOTH, expand=1)
		wTopJoinBtn = PanedWindow(mainWindow)
		wTopScrolls = PanedWindow(mainWindow)
		wTopSubmit  = PanedWindow(mainWindow)
		wBotScroll  = PanedWindow(mainWindow)
		wBotSubmit  = PanedWindow(mainWindow)
		mainWindow.add(wTopJoinBtn)
		mainWindow.add(wTopScrolls)
		mainWindow.add(wTopSubmit)
		mainWindow.add(wBotScroll)
		mainWindow.add(wBotSubmit)
		# TOP JOIN BUTTON
		self._joinBtn(wTopJoinBtn)
		# TOP SCROLLABLES
		self.users, self.files = self._createTopScrolls(wTopScrolls)
		# SEND FILE BUTTON
		self._sendBtn(wTopSubmit)
		# BOTTOM SCROLLABLE
		self.downloadables = self._createBotScroll(wBotScroll)
		# DOWNLOAD BUTTON
		self._downloadBtn(wBotSubmit)

	def _joinBtn(self, wTopJoinBtn):
		btn = Button(wTopJoinBtn, text = "Find devices", command = self._joinMCast)
		btn.pack()
		wTopJoinBtn.add(btn)

	def _joinMCast(self):
		multicast.rejoin(self.MCAST_GROUP, self.MCAST_PORT)

	def _createTopScrolls(self, wTopScrolls):
		wLeftScroll  = PanedWindow(wTopScrolls)
		wRightScroll = PanedWindow(wTopScrolls)
		wTopScrolls.add(wLeftScroll)
		wTopScrolls.add(wRightScroll)
		scrollUsers = Scrollbar(wLeftScroll)
		scrollUsers.pack( side = RIGHT, fill = Y )
		scrollFiles = Scrollbar(wRightScroll)
		scrollFiles.pack( side = RIGHT, fill = Y )
		myUsers = Listbox( wLeftScroll, yscrollcommand = scrollUsers.set )
		myFiles = Listbox( wRightScroll, yscrollcommand = scrollFiles.set )
		myUsers.pack( side = LEFT, fill = BOTH )
		scrollUsers.config( command = myUsers.yview )
		myFiles.pack( side = LEFT, fill = BOTH )
		scrollFiles.config( command = myFiles.yview )
		return (myUsers, myFiles)

	def _sendBtn(self, wTopSubmit):
		btn = Button(wTopSubmit, text = "Send", command = self._send)
		btn.pack()
		wTopSubmit.add(btn)

	def _createBotScroll(self, wBotScroll):
		scrollDownloadables = Scrollbar(wBotScroll)
		scrollDownloadables.pack( side = RIGHT, fill = Y )
		myDownloadables = Listbox( wBotScroll, yscrollcommand = scrollDownloadables.set )
		scrollDownloadables.config( command = myDownloadables.yview )
		myDownloadables.pack( fill = BOTH )
		return myDownloadables

	def _downloadBtn(self, wBotSubmit):
		btn = Button(wBotSubmit, text = "Download", command = lambda: self._download(downloadables))
		btn.pack()
		wBotSubmit.add(btn)

	def _send(self):
		print "send!"

	def _download(self, downloadables):
		print "download!"

	def start(self):
		# Start mainloop
		mainloop()		

	def newDownloadable(self, newDwn):
		self.downloadables.insert(END, str(newDwn))

	def newUser(self, newUsr):
		self.users.insert(END, str(newUsr))

	def newFile(self, newF):
		self.files.insert(END, str(newF))