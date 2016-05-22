import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2

'''
    Takes a list of pictures and saves it to a AVI-video file
    
'''

class RecordVideoMod():
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def makeVideo(self, theList, occured, fps):
        theText = occured +".avi"
        #For use on raspberry
        vw = cv2.VideoWriter(theText, cv2.cv.CV_FOURCC('M', 'J', 'P', 'G'), fps, (self.width,self.height))
        #For use in windows
        #vw = cv2.VideoWriter(theText, cv2.VideoWriter_fourcc(*'XVID'), 10.0, (640,480))

        for im in theList:
            vw.write(im)
        vw.release()
