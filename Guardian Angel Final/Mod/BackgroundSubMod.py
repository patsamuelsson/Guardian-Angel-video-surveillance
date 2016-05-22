

import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2
import numpy as np
import datetime

'''
    Mod for removing the background and then draw the contour
    of the biggest moving object thats between a set amount of points
    so it doesnt draw noise or disturbances.
'''

class BackgroundSubMod:
    def __init__(self, width, height):

        self.width = width
        self.height = height

        #Backgroundsubtractor for real computers
        #self.fgbg = cv2.createBackgroundSubtractorMOG2(10, 8, False)
        #Backgroundsubtractor for the PI
        self.fgbg = cv2.BackgroundSubtractorMOG2(10, 64, False)

        self.maxX = 0
        self.minX = 0

        self.picChangeTime = None
        self.first = True
        self.currCont = None
        self.biggestCont = None
        self.prevBigId = None
        self.kernel = np.ones((3,3), 'uint8')

        self.blackImg = None
        self.normImg = None

        #Contour settings
        self.maxCont = 0
        self.minCont = 0

    '''
        Function were you send in a picture and if you want a black image with the contours drawn
        or if you want to get just the picture were you get a rectangle around the biggest
        moving contour, most often a person.
    '''

    def apply(self, cv2img, blackImg):

        """
            Get the background subtracted image
            learningRate defines how long something has to be in the picture to be considered as background.
        """
        fgmask = self.fgbg.apply(cv2img, learningRate=0.04)
        '''
            After we get the background subtracted image, we use 2 commands
            to Erode and dialate in the first and then dialate and erode the image
            on the second, this helps remove small noise and errors.
        '''
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, self.kernel)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, self.kernel)

        #Look for all contours that exists (If on a real computer need 3 variables add 1 BEFORE self.currentCont, pi need 2)
        self.currCont, hierachy = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        #Find the biggest contour
        largestArea = 0
        largestContInd = 0
        i = 0
        for cnt in self.currCont:
            if len(cnt)>largestArea:
                largestArea = len(cnt)
                largestContInd = i
            i+=1

        #Make an empty black img, same size as the one sent in
        height, width = fgmask.shape
        img = np.zeros((height, width, 3), np.uint8)

        #Check how many points long the biggest contour is.
        if len(self.currCont) == 0:
            leng = 0;
        else:
            leng = len(self.currCont[largestContInd])
            

        #Draw the rectangle around the biggest contour and/or draw the contours onto the black image.
        if not self.first:
            if leng != 0:
                self.maxX = 0
                self.minX = self.width
                for cnt in self.biggestCont:
                    x=cnt[0][0]
                    if x < self.minX:
                        self.minX = x
                    if x > self.maxX:
                        self.maxX = x

            '''
                Return the image wanted, either the blackimage with just the contour or
                the normal image with the contour inside a rectangle.
            '''
            if blackImg:
                if leng < self.maxCont and leng > self.minCont:
                    self.picChangeTime = datetime.datetime.now()
                    cv2.drawContours(img, self.currCont, largestContInd,(255,0,255), 2)
                    #cv2.rectangle(img,(self.minX, self.minY),(self.maxX, self.maxY),(255,255,0),2)
                    self.biggestCont = self.currCont[largestContInd]
                else:
                    now = datetime.datetime.now()
                    tdelta = now - self.picChangeTime
                    secs = tdelta.total_seconds()
                    if secs <= 4:
                        cv2.drawContours(img, self.biggestCont, -1,(0,255,255), 2)
                        #cv2.rectangle(img,(self.minX, self.minY),(self.maxX, self.maxY),(255,255,0),2)
                return img
            else:
                if leng < self.maxCont and leng > self.minCont:
                    self.picChangeTime = datetime.datetime.now()
                    cv2.rectangle(cv2img,(self.minX, 0),(self.maxX, self.height),(255,255,0),2)
                    self.biggestCont = self.currCont[largestContInd]
                else:
                    now = datetime.datetime.now()
                    tdelta = now - self.picChangeTime
                    secs = tdelta.total_seconds()
                    if ((self.maxX > self.width-10 and secs >= 4) or (self.minX < 10 and secs >= 4)):
                        None
                    else:
                        cv2.rectangle(cv2img,(self.minX, 0),(self.maxX, self.height),(255,255,0),2)
                return cv2img

        #Dont draw a rectangle or the contours the first time.
        if self.first:
            self.picChangeTime = datetime.datetime.now()
            self.biggestCont = self.currCont[largestContInd]
            self.first = False
            return cv2img
