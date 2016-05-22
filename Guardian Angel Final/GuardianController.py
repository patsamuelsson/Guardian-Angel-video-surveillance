
from Mod.PicMod import PicMod
from Mod.FtpUploadMod import FtpUploadMod
from View.MainView import MainView
from Mod.ConvertImageMod import ConvertImageMod
from Mod.PaintRectMod import PaintRectMod
from Mod.RecordVideoMod import RecordVideoMod
from Mod.BackgroundSubMod import BackgroundSubMod
from Data.myRectangle import myRectangle
from Mod.mysqlMod import mysqlMod
from Mod.EventMod import EventMod
from Tkinter import *
import threading
import datetime
import time
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2
'''
    Controller for Guardian Angel Video Surveillence
	
	Made by Patrik Samuelsson and Oskar Gustavsson 

'''

class GuardianController:
    '''
        Initialize all mods and variables for use
    '''
    def __init__(self, tk, width, height, testMode, fps):
        self.width = width
        self.height = height
        self.tk = tk
        self.fps = fps
        self.testMode = testMode
        self.pMod = PicMod(width, height)
        self.cv2Image = self.pMod.takePic()
        self.backgroundMod = BackgroundSubMod(width, height)
        self.recMod = RecordVideoMod(width, height)
        self.cMod = ConvertImageMod(self.cv2Image)
        self.tkImage = self.cMod.cv2ToImage(self.cv2Image)
        self.paintRectMod = PaintRectMod(self.cv2Image)
        self.mView = MainView(tk, self.tkImage, width, height, self.testMode)
        self.uploadM = FtpUploadMod()
        self.databaseM = mysqlMod()
        self.eventM = EventMod(myRectangle(0,0,0,0,"fake", 5))
        self.startupSettings()
        self.rectList = []
        self.startupRects()
        self.imageList = []
        self.counter = 0
        self.tk.after(0, self.updateLabel())

    '''
        Set the first picture in tkinter
    '''
    def updateLabel(self):
        self.mView.setPic(self.tkImage)
        self.tk.after(100, func=lambda :self.updateLabel())
    """
        sets up the sideRectangles 
    """
    def startupRects(self):
        right = myRectangle(0,2,10,self.height,"Left", 2)
        left = myRectangle(self.width-10,0,self.width,self.height,"Right", 2)
        self.rectList.append(left)
        self.rectList.append(right)

    """
        Read in the saved settings from file and set them
        in the mods.
    """
    def startupSettings(self):
        file = open('Data/settings.txt', 'r')
        tmp = 0
        for line in file:
            if tmp == 0:
                self.backgroundMod.maxCont = int(line)
                self.mView.setSetting(str(self.backgroundMod.maxCont), 1)
            if tmp == 1:
                self.backgroundMod.minCont = int(line)
                self.mView.setSetting(str(self.backgroundMod.minCont), 2)
            if tmp == 2:
                self.eventM.timeEvent = int(line)
                self.mView.setSetting(str(self.eventM.timeEvent), 3)
            tmp+=1
    """
        Function for changing settings
    """
    def settingChange(self, sett):
        if sett == 1:
            self.backgroundMod.maxCont+=10
            self.mView.setSetting(str(self.backgroundMod.maxCont), 1)
        if sett == 2:
            if self.backgroundMod.maxCont > self.backgroundMod.minCont+10:
                self.backgroundMod.maxCont-=10
            self.mView.setSetting(str(self.backgroundMod.maxCont), 1)
        if sett == 3:
            if self.backgroundMod.minCont < self.backgroundMod.maxCont-10:
                self.backgroundMod.minCont+=10
            self.mView.setSetting(str(self.backgroundMod.minCont), 2)
        if sett == 4:
            if self.backgroundMod.minCont > 10:
                self.backgroundMod.minCont-=10
            self.mView.setSetting(str(self.backgroundMod.minCont), 2)
        if sett == 5:
            self.eventM.timeEvent += 1
            self.mView.setSetting(str(self.eventM.timeEvent), 3)
        if sett == 6:
            if self.eventM.timeEvent > 0:
                self.eventM.timeEvent -= 1
            self.mView.setSetting(str(self.eventM.timeEvent), 3)

    '''
        Save all settings
    '''
    def saveSettings(self):
        file = open("Data/settings.txt", 'w')
        file.write(str(self.backgroundMod.maxCont)+"\n")
        file.write(str(self.backgroundMod.minCont)+"\n")
        file.write(str(self.eventM.timeEvent)+"\n")

'''
    Startup thread, this thread just shows the first image.
    All tools enabled including: marking areas, changing settings,
    renaming areas, undo areas.
'''
class StartupThread(threading.Thread):
    def __init__(self, gc, mt):
        super(StartupThread, self).__init__()
        self.gc = gc
        self.mt = mt
        self.quit = False
        self.t1 = None
        self.t2 = None

    def run(self):
        #Startup Mode, get areas of interest coords
        while not gc.mView.start:
            try:
                if self.gc.mView.quit:
                    self.gc.saveSettings()
                    self.gc.pMod.releaseCam()
                    self.gc.tk.destroy()
                    self.gc.mView.start = True
                    self.quit = True

                xPos = self.gc.mView.getXpos()
                yPos = self.gc.mView.getYpos()
                endXPos = self.gc.mView.getEndXpos()
                endYPos = self.gc.mView.getEndYpos()

                # if Done, start mainThread to start analyzing pictures.
                if self.gc.mView.done:
                    tmp = self.gc.mView.buttChange
                    if tmp == -1:
                        self.gc.rectList.append(myRectangle(xPos, yPos, endXPos, endYPos, self.gc.mView.rectNames[self.gc.mView.numbRect-1], self.gc.mView.rbMode.get()))
                        #Reset position of x and y
                        self.gc.mView.resetPos()
                    if tmp != -1:
                        self.gc.rectList[tmp+2].id = self.gc.mView.rectNames[tmp]
                        self.gc.mView.buttChange = -1
                    self.gc.tkImage = self.gc.paintRectMod.paintRectList(self.gc.rectList)
                    self.gc.mView.done = False

                #Undo last triangle?
                if self.gc.mView.undo:
                    if len(self.gc.rectList) != 0:
                        self.gc.rectList.pop()


                #If clicked and dragged redraw the rectangle
                if self.gc.mView.marking or self.gc.mView.undo:
                    self.gc.tkImage = self.gc.paintRectMod.paintRect(xPos, yPos, endXPos, endYPos, self.gc.rectList)
                    self.gc.mView.undo = False
                time.sleep(0.1)

                #Setting changed?
                sett = self.gc.mView.setting
                if sett != 0:
                    self.gc.settingChange(sett)

            except Exception as e:
                print "Startup Thread EXCEPTION"
                print e

        print "Start Thread ended"
        if not self.quit:
            self.mt.start()

'''
    The thread for analyzing pictures and generating events.
    Tools available are settings and quit, rest are disabled.
'''
class MainThread(threading.Thread):
    def __init__(self, gc):
        super(MainThread, self).__init__()
        self.gc = gc
        self.event = False
        self.currImg = None
        self.frames = 0
        self.seconds = 0
        self.counter = 0
        self.timeLastEvent = 0
        self.first = True
        self.fps = self.gc.fps
        self.secCounter = 0
        self.countUp = 1
      

    def run(self):
        print "Main Thread Started"

        #Take 10 pictures before starting to learn the background
        for i in range(10):
            self.currImg = self.gc.pMod.takePic()

        while True:
            t1 = time.time();
            #Quit?
            if self.gc.mView.quit:
                self.gc.saveSettings()
                self.gc.pMod.releaseCam()
                self.gc.tk.destroy()
                self.gc.mView.start = True
                self.quit = True

            #Setting changed?
            sett = self.gc.mView.setting
            if sett != 0:
                self.gc.settingChange(sett)

            #Picture analysis
            self.currImg = self.gc.pMod.takePic()
            self.currImg = self.gc.backgroundMod.apply(self.currImg, False)

            #Check if inside rectangle, set that rectangle to active
            if not self.first:
                for rect in self.gc.rectList:
                    counter = 0
                    for cnt in self.gc.backgroundMod.biggestCont:
                        x = cnt[0][0]
                        if x > rect.xPos and x < rect.endXPos and len(self.gc.backgroundMod.biggestCont)!=4:
                            if not rect.active:
                                rect.timeActive = datetime.datetime.now()
                            rect.active = True
                            counter+=1
                    if counter == 0:
                        rect.active = False

            #First time running the loop, here to not do any pic analysis on the first run
            if self.first:
                self.first = False

            if self.gc.testMode:
                self.gc.paintRectMod.setPic(self.currImg)
                self.gc.tkImage = self.gc.paintRectMod.paintRectList(self.gc.rectList)

            #List were we save all the images.
            if len(self.gc.imageList) < self.fps * 30:
                self.gc.imageList.append(self.currImg)
            if len(self.gc.imageList) == self.fps * 30:
                self.gc.imageList.pop(0)
                self.gc.imageList.append(self.currImg)

            # Check if an event has occured, atleast 5 seconds between each event.
            if self.timeLastEvent > 25:
                self.gc.eventM.checkEvents(self.gc.rectList)
                if self.gc.eventM.sEvent != '':
                    self.event =  True
                    cv2.putText(self.currImg, "Event", (0,90) , cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255))
                    self.gc.imageList.pop(0)
                    self.gc.imageList.append(self.currImg)
                    ev = EventThread(self.gc, self.gc.eventM.sEvent, self.fps)
                    self.gc.eventM.sEvent = ''

            #After generating an event reset the event variables.
            if self.event:
                self.event = False
                self.timeLastEvent = 0
                ev.start()

            #Count pictures since last event
            self.timeLastEvent += 1

            #Regulate fps
            t2 = time.time()
            tmp = t2 - t1
            sleeptime = (1/float(self.fps))-tmp
            if sleeptime > 0:
                time.sleep(sleeptime);
            
            
"""
    EventThread, starts when an event is detected.
    Saves the video, uploads it to the ftp server and updates the database
"""

class EventThread(threading.Thread):
    def __init__(self, gc, theEvent, fps):
        super(EventThread, self).__init__()
        self.gc = gc
        self.gc.counter+=1
        self.id = 1
        self.videoid = self.gc.counter
        self.theList = []
        self.theEvent = theEvent
        self.fps = fps


    def run(self):
        if self.gc.testMode:
            self.gc.mView.setInfo(self.theEvent)
        print self.theEvent

        #Wait 15 seconds after the event occured
        time.sleep(15)

        if self.gc.testMode:
            self.gc.mView.setInfo("Saving video...")
        self.theList = list(self.gc.imageList)
        vidname = str(self.id) + "_" + str(self.videoid)

        #Save the video
        self.gc.recMod.makeVideo(self.theList, vidname, self.fps)
        if self.gc.testMode:
            self.gc.mView.setInfo("Video Successfully Saved!, uploading to FTP...")

        #Upload to FTP
        self.gc.uploadM.upload(vidname)
        if self.gc.testMode:
            self.gc.mView.setInfo("Video Successfully Uploaded. Updating Database.")

        #Upload to database
        self.gc.databaseM.updateDb(vidname, self.id, self.theEvent)
        if self.gc.testMode:
            self.gc.mView.setInfo("Event Successfully Completed all Sending")
        
        
'''
    Start point for the program, starts initialization and setup
'''

if __name__ == "__main__":
    tk = Tk()
    gc = GuardianController(tk, 320, 180, True, 5)
    mainThread = MainThread(gc)
    startupThread = StartupThread(gc, mainThread)
    startupThread.start()
    tk.mainloop()
