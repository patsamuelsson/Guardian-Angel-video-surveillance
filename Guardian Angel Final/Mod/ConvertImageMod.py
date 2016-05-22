

from PIL import Image, ImageTk

'''
    Mod for converting image from Cv2-image
    to an image that can be shown and handled
    by tkinter
'''

class ConvertImageMod():
    def __init__(self, pic):
        self.currImg = pic

    def cv2ToImage(self, cv2Img):
        self.currImg = Image.fromarray(cv2Img)
        self.currImg = ImageTk.PhotoImage(image=self.currImg)
        return self.currImg