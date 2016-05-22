import datetime

'''
    Rectangle objects or areas of interests.
    Contains start and end coords for the marked areas
'''

class myRectangle():
    def __init__(self, xPos, yPos, endXPos, endYPos, id, mode):
        self.id = id
        self.xPos = xPos
        self.yPos = yPos
        self.endXPos = endXPos
        self.endYPos = endYPos
        self.active = False
        self.timeActive = None

        # 0 = No event has happend
        # 1 = Event has happend
        self.state = 0

        # 0 = Area of Interest
        # 1 = Door
        # 2 = Side Area
        self.mode = mode