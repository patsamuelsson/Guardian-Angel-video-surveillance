import datetime

'''
    Mod for checking if an event has occured.
'''

class EventMod():
    def __init__(self, fakeRec):
        self.sEvent = ''
        self.fakeRec = fakeRec
        self.lastActive = fakeRec
        self.currActive = fakeRec
        self.anyActive = fakeRec
        self.timeEvent = 0

    def checkEvents(self, rectlist):
        now = datetime.datetime.now()

        #Any active Doors or side rectangles?
        for rect in rectlist:
            if rect.active:
                self.anyActive = rect
                if rect.active and rect.mode == 1 or rect.mode == 2:
                    self.currActive = rect
                else:
                    self.currActive = self.fakeRec
                    self.anyActive = self.fakeRec

        #Same rectangle active?
        if self.currActive.id == self.lastActive.id or self.currActive.id == self.fakeRec.id:
            same = True
        else:
            same = False

        for rect in rectlist:
            #Events for an Area of Interest
            if rect.mode == 0:
                if rect.active and rect.state == 0:
                    tdelta = now - rect.timeActive
                    secs = tdelta.total_seconds()
                    if secs > self.timeEvent:
                        rect.state = 1
                        self.sEvent = "Went to " + str(rect.id)
                elif not rect.active and rect.state == 1:
                    rect.timeActive = None
                    rect.state = 0
                    if self.anyActive.mode == 1 or self.anyActive.mode == 2:
                        self.sEvent = "Went to " + str(self.anyActive.id)
                        self.anyActive.state = 1
                    else:
                        self.sEvent = "Left " + str(rect.id)

            #Events for a door and siderectangles
            if rect.mode == 1 or rect.mode == 2:
                if rect.active and rect.state == 0:
                    tdelta = now - rect.timeActive
                    secs = tdelta.total_seconds()
                    if secs > self.timeEvent:
                        rect.state = 1
                        self.lastActive = rect
                        self.sEvent = "Went to " + str(rect.id)
                elif not rect.active and not same and rect.state == 1:
                    rect.timeActive = None
                    self.sEvent = "Came back from " + str(self.currActive.id)
                    for rect in rectlist:
                        if rect.mode == 1 or rect.mode == 2:
                            rect.state = 0
                elif not rect.active and rect.state == 1:
                    rect.timeActive = None
                    self.sEvent = "Came back from " + str(rect.id)
                    rect.state = 0
