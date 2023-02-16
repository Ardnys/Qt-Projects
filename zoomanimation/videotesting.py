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
        camera = cv2.VideoCapture(0) # 0 is webcam local camera or smth
        while self.threadactive:
            okay, frame = camera.read()
            if okay:
                # the type of frame is numpy array 
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                flippedimage = cv2.flip(image, 1)
                qtimage = QtGui.QImage(flippedimage.data, flippedimage.shape[1], flippedimage.shape[0], QtGui.QImage.Format_RGB888)
                picture = qtimage.scaled(480, 360, QtCore.Qt.KeepAspectRatio)
                self.videoupdate.emit(picture)
                      
    
    def stop(self):
        self.threadactive = False
        self.quit()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())