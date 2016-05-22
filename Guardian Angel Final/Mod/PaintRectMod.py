
from Data.myRectangle import myRectangle
from PIL import Image, ImageTk, ImageDraw

'''
    Paints the rectangle on the image.
    Must be a CV2Image
'''

class PaintRectMod():
    def __init__(self, pic):
        self.theImg = Image.fromarray(pic)

    #Paints the currently painting rectangle and all saved rectangles
    def paintRect(self, xPos, yPos, endXPos, endYPos, rectlist):
        try:
            tmpimg = self.theImg.copy()
            if xPos != 0 and yPos != 0 and endYPos != 0 and endXPos != 0:
                dr = ImageDraw.Draw(tmpimg)
                dr.rectangle(((xPos, yPos), (endXPos, endYPos)), outline="blue")
                xCent = (xPos + endXPos)/2
                yCent = (yPos + endYPos)/2
                dr.text((xCent, yCent), "Painting...", fill="red")

            if len(rectlist) != 0:
                color = None
                for rect in rectlist:
                    if rect.mode == 0:
                        color = "red"
                    elif rect.mode == 1:
                        color = "orange"
                    else:
                        color = "white"
                    dr = ImageDraw.Draw(tmpimg)
                    dr.rectangle(((rect.xPos, rect.yPos), (rect.endXPos, rect.endYPos)), outline=color)
                    xCent = (rect.xPos + rect.endXPos)/2
                    yCent = (rect.yPos + rect.endYPos)/2
                    dr.text((xCent, yCent), rect.id, fill="yellow")
            tmpimg = ImageTk.PhotoImage(image=tmpimg)
            return tmpimg

        except Exception:
            print "Couldnt paint rect"
            return self.theImg

    def paintRectList(self, rectlist):
        tmpimg = self.theImg.copy()
        if len(rectlist) != 0:
            for rect in rectlist:
                dr = ImageDraw.Draw(tmpimg)
                if rect.active:
                    dr.rectangle(((rect.xPos, rect.yPos), (rect.endXPos, rect.endYPos)), outline="green")
                else:
                    color = None
                    if rect.mode == 0:
                        color = "red"
                    elif rect.mode == 1:
                        color = "orange"
                    else:
                        color = "white"
                    dr.rectangle(((rect.xPos, rect.yPos), (rect.endXPos, rect.endYPos)), outline=color)
                xCent = (rect.xPos + rect.endXPos)/2
                yCent = (rect.yPos + rect.endYPos)/2
                dr.text((xCent, yCent), rect.id, fill="yellow")
        tmpimg = ImageTk.PhotoImage(image=tmpimg)
        return tmpimg

    def setPic(self, pic):
         self.theImg = Image.fromarray(pic)