
import ftplib
import os


"""
    Connects with the ftpserver and uploads the video to it
    after upload the video is deleted from the raspberry
"""

class FtpUploadMod():
    def __init__(self):
        None

    def upload(self, vidName):
        session = ftplib.FTP('#.#.#.#', 'raspberry', '')
        file = open(vidName + ".avi", 'rb')
        namn = 'STOR Name/' + vidName + '.avi'
        session.storbinary(namn, file)
        file.close()
        session.quit()
        os.remove(vidName+ '.avi')
