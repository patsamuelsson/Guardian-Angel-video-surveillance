
''' Main View for marking up
    areas of interest and choose
    settings for event detection '''

from Tkinter import *

class MainView:

    #Setup the starting view with no settings
    def __init__(self, tk, theImage, width, height, testMode):

        #/ General variable assignment \#
        self.theImage = theImage
        self.reserveImg = theImage
        self.xPos = 0
        self.yPos = 0
        self.endXpos = 0
        self.endYpos = 0
        self.buttChange = -1
        self.WIDTH = width
        self.HEIGHT = height
        self.start = False
        self.done = False
        self.undo = False
        self.marking = False
        self.quit = False
        self.rectLabels = []
        self.rectNames = []
        self.renameButt = []
        self.buttID = [1,2,3,4,5]
        self.numbRect = 0
        self.testMode = testMode
        self.rbMode = IntVar()
        self.setting = 0

        #/ Main view \#
        # Title and center its position on the screen
        self.tk = tk
        self.tk.title("Guardian Angel v1.0 FINAL beta")

        #/ Frames \#
        # Split the view in two, top and bottom
        self.topF = Frame(tk)
        self.topF.grid(column=0, row=0)

        self.botF = Frame(tk)
        self.botF.grid(column=0, row=1, columnspan=2)

        self.sideF = Frame(tk)
        self.sideF.grid(column=1, row=0)

        #/ Labels \#

        #Settings
        self.conSet = Label(self.sideF, text="Contour Settings")
        self.conSet.grid(row=0, column=0, columnspan=3)

        self.maxCon = Label(self.sideF, text="600")
        self.maxCon.grid(row=1, column=1)

        self.minCon = Label(self.sideF, text="120")
        self.minCon.grid(row=2, column=1)

        self.conSet = Label(self.sideF, text="Time until event occurs")
        self.conSet.grid(row=3, column=0, columnspan=3)

        self.eventTimeL = Label(self.sideF, text="2")
        self.eventTimeL.grid(row=4, column=1)

        #Shows the first image, used for marking areas of interest
        self.picL = Label(self.topF, image=self.theImage,bg="black")
        self.picL.bind("<ButtonPress-1>", self.mClicked)
        self.picL.bind("<B1-Motion>", self.mMove)
        self.picL.bind("<ButtonRelease-1>", self.mRelease)
        self.picL.grid(column=0, row=0, columnspan=2)

        #Label for showing information
        self.infoL = Label(self.botF, text="Information: ")
        self.infoL.grid(column=0, row=6, columnspan=3, sticky=W)

        #Shows the rectangles
        for lab in range(5):
            tmp = Label(self.botF, text="Area of Interest: ")
            tmp.grid(column = 0, row = lab, sticky=W)
            self.rectLabels.append(tmp)

        #/ RadioButtons \#

        #Choose if marking a door or Area of Interes
        self.rbArea = Radiobutton(master=self.topF, text='Area of Interest', variable=self.rbMode, value=0).grid(row=1, column=0)
        self.rbDoor = Radiobutton(master=self.topF, text='Door', variable=self.rbMode, value=1).grid(row=1, column=1)

        #/ Buttons \#

        #Settings
        #Contour settings
        self.incMaxCont = Button(self.sideF, text="+", width=5, height=2, command=lambda : self.changeSetting(1))
        self.incMaxCont.grid(row=1, column=2)

        self.decMaxCont = Button(self.sideF, text="-", width=5, height=2, command=lambda : self.changeSetting(2))
        self.decMaxCont.grid(row=1, column=0)

        self.incMinCont = Button(self.sideF, text="+", width=5, height=2, command=lambda : self.changeSetting(3))
        self.incMinCont.grid(row=2, column=2)

        self.decMinCont = Button(self.sideF, text="-", width=5, height=2, command=lambda : self.changeSetting(4))
        self.decMinCont.grid(row=2, column=0)

        #Event time settings
        self.incEventTime = Button(self.sideF, text="+", width=5, height=2, command=lambda : self.changeSetting(5))
        self.incEventTime.grid(row=4, column=2)

        self.decEventTime = Button(self.sideF, text="-", width=5, height=2, command=lambda : self.changeSetting(6))
        self.decEventTime.grid(row=4, column=0)

        #Start the video surveillance
        self.startB = Button(self.botF, text="Start", width=20, height=2, command=self.startPressed)
        self.startB.grid(row=5, column=0)

        #Manual event
        self.quitB = Button(self.botF, text="Quit", width=20, height=2, command=self.quitPressed)
        self.quitB.grid(row=5, column=2)

        #Remove last rectangle
        self.undoB = Button(self.botF, text="Undo", width=20, height=2, command=self.undoPressed)
        self.undoB.grid(row=5, column=1)

        #Rename Buttons
        #1
        tmp = Button(self.botF, text="Rename", state = DISABLED, command=lambda : self.rename(0))
        tmp.grid(row=0, column=2)
        self.renameButt.append(tmp)
        #2
        tmp = Button(self.botF, text="Rename", state = DISABLED, command=lambda : self.rename(1))
        tmp.grid(row=1, column=2)
        self.renameButt.append(tmp)
        #3
        tmp = Button(self.botF, text="Rename", state = DISABLED, command=lambda : self.rename(2))
        tmp.grid(row=2, column=2)
        self.renameButt.append(tmp)
        #4
        tmp = Button(self.botF, text="Rename", state = DISABLED, command=lambda : self.rename(3))
        tmp.grid(row=3, column=2)
        self.renameButt.append(tmp)
        #5
        tmp = Button(self.botF, text="Rename", state = DISABLED, command=lambda : self.rename(4))
        tmp.grid(row=4, column=2)
        self.renameButt.append(tmp)

    '''
        Change the picture thats in the label
    '''
    def setPic(self, newImage):
        try:
            self.theImage = newImage
            self.picL.configure(image=self.theImage)
        except Exception as ex:
            print "Couldnt set Image"
            print ex

    #Change the information that shows what has happend
    def setInfo(self, newString):
        self.infoL.configure(text="Information: " + newString)

    #Show the current setting of Contours and time since last event
    def setSetting(self, newString, id):
        if id == 1:
            self.maxCon.configure(text=newString)
        if id == 2:
            self.minCon.configure(text=newString)
        if id == 3:
            self.eventTimeL.configure(text=newString)
        self.setting = 0

    '''
        Set the x and y coords to were the mouse were clicked on the label
    '''
    def mClicked(self, event):
        if self.numbRect < 5:
            self.marking = True
            self.endXpos = 0
            self.endYpos = 0
            self.xPos = event.x
            self.yPos = event.y

    '''
        While dragging the mouse update x and y end-coords until mousebutton is released
    '''
    def mMove(self, event):
        try:
            if self.numbRect < 5:
                self.endXpos = event.x
                self.endYpos = event.y
        except Exception as ex:
            print "Mouse Movement Not Registered Correctly"
            print ex

    '''
        When button is released the rectangle is done and needs to be saved
    '''
    def mRelease(self, event):
        if self.numbRect < 5:
            self.marking = False
            self.done = True
            tmp = "Area: " + str(self.numbRect+1)
            self.rectNames.append(tmp)
            self.rectLabels[self.numbRect].config(text=self.rectNames[self.numbRect])
            self.renameButt[self.numbRect].config(state=NORMAL)
            self.numbRect += 1

    '''
        Functions for the controller to get x and y coords
    '''
    def getXpos(self):
        return self.xPos

    def getYpos(self):
        return self.yPos

    def getEndXpos(self):
        return self.endXpos

    def getEndYpos(self):
        return self.endYpos

    def resetPos(self):
        self.xPos = 0
        self.yPos = 0
        self.endXpos = 0
        self.endYpos = 0

    '''
        Button functions
    '''

    #Quit program, destroys TK and releases camera
    def quitPressed(self):
        self.quit = True

    #Setting changed
    def changeSetting(self, settId):
        self.setting = settId

    #Start Video Surv.
    def startPressed(self):
        self.undoB.configure(state=DISABLED)
        self.startB.configure(state=DISABLED)
        for butt in self.renameButt:
            butt.configure(state = DISABLED)
        self.start = True
        if not self.testMode:
            self.tk.destroy()

    #Undo last area of interest
    def undoPressed(self):
        if self.numbRect > 0:
            self.numbRect -= 1
            self.rectLabels[self.numbRect].config(text="Area of interest: ")
            self.renameButt[self.numbRect].config(state=DISABLED)
            self.undo = True

    #Rename popup
    def rename(self, bId):
        top = Toplevel()
        top.title("Rename Area")
        entr = Entry(top, width=20)
        entr.pack()
        topButt = Button(top, text="Done", command=lambda : self.renameDone(top, entr, bId))
        topButt.pack()

    def renameDone(self, top, entr, bId):
        tmpStr = entr.get()
        self.rectLabels[bId].config(text=tmpStr)
        self.rectNames[bId]=tmpStr
        self.buttChange = bId
        self.done = True
        top.destroy()
