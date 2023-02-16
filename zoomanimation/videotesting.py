from PyQt5 import QtGui, QtCore, QtWidgets, uic
import sys, cv2

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('customgraphtest.ui', self)

        # connect buttons
        self.startbutton.clicked.connect(self.startstream)
        self.stopbutton.clicked.connect(self.endstream)

        self.thread = VideoThread()
        self.thread.videoupdate.connect(self.imageupdateslot)

    def imageupdateslot(self, image):
        self.videolabel.setPixmap(QtGui.QPixmap.fromImage(image))

    def startstream(self):
        self.thread.start()

    def endstream(self):
        self.thread.stop()

class VideoThread(QtCore.QThread):
    videoupdate = QtCore.pyqtSignal(QtGui.QImage)
    def run(self) -> None:
        self.threadactive = True
        self._camera = cv2.VideoCapture(0) # 0 is webcam local camera or smth
        
        # parameters for output video
        HEIGHT = 480
        WIDTH = 640
        FPS = 30.0

        # set camera settings if needed

        # self._camera.set(cv2.CAP_PROP_CONVERT_RGB , 1)
        # self._camera.set(cv2.CAP_PROP_BUFFERSIZE, 100)
        # self._camera.set(cv2.CAP_PROP_FPS, FPS)
        # self._camera.set(3, WIDTH)
        # self._camera.set(4, HEIGHT)
        

        fourcc = cv2.VideoWriter_fourcc(*'XVID') # XVID for .avi, mp4v for .mp4 format
        # output parameters such as fps and size can be changed
        self._output = cv2.VideoWriter("output.avi", fourcc, FPS, (WIDTH, HEIGHT))
        # further frustration reading: https://stackoverflow.com/questions/30509573/writing-an-mp4-video-using-python-opencv

        """
        VideoCapture takes about 1.5 seconds to initialise
        setting WIDTH, HEIGHT, and FPS takes about 3.7 seconds to set
        settings everything takes 4.9 seconds to set
        the video didn't work when i didn't do those but now it works without setting anything"""

        while self.threadactive:
            okay, frame = self._camera.read()
            if okay:
                # the type of frame is numpy array 
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                flippedimage = cv2.flip(image, 1)

                # write the flipped frame without any processing
                self._output.write(cv2.flip(frame, 1))

                qtimage = QtGui.QImage(flippedimage.data, flippedimage.shape[1], flippedimage.shape[0], QtGui.QImage.Format_RGB888)
                picture = qtimage.scaled(640, 480, QtCore.Qt.KeepAspectRatio)
                self.videoupdate.emit(picture)
                      
    
    def stop(self):
        self.threadactive = False
        # release the objects idk what they do
        self._camera.release()
        self._output.release()
        self.quit()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())