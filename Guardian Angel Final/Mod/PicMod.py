
import numpy
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2

''' Mod for taking Pictures from the webcam '''

class PicMod():
    #Init the camera and set capture size.
    def __init__(self, width, height):
        self.cam = cv2.VideoCapture(0)
        self.cam.set(3, width)
        self.cam.set(4, height)

    #Takes a picture as cv2image and makes it grey then returns
    def takePic(self):
        s, cv2img = self.cam.read()
        if not s:
            print "No picture taken"
        #cv2img = cv2.cvtColor(cv2img, cv2.COLOR_BGR2GRAY)
        return cv2img

    def releaseCam(self):
        self.cam.release()