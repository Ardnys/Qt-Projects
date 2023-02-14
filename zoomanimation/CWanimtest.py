from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

class PGraph(PlotWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._initial_size = self.size()
        self._zoomed_size = QtCore.QSize(self._initial_size.width()+50, self._initial_size.height()+50)

        self._animation = QtCore.QPropertyAnimation(
            self, b"size",
            startValue=self._initial_size,
            endValue=self._zoomed_size,
            duration=400
        )
        # self.setMinimumSize(QtCore.QSize(200,150))
        # self.resize(200,150)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        # self.setSizePolicy(sizePolicy)
    
    def updateAnimation(self, startval: QtCore.QSize, endval: QtCore.QSize):
        self._animation = QtCore.QPropertyAnimation(
            self, b"size",
            startValue=startval,
            endValue=endval,
            duration=400
        )

    def enterEvent(self, event):
        self._animation.setDirection(QtCore.QAbstractAnimation.Forward)
        self._animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._animation.setDirection(QtCore.QAbstractAnimation.Backward)
        self._animation.start()
        super().leaveEvent(event)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        if self._animation.state() == 2:
            return super().paintEvent(a0)
        elif self._animation.state() == 0:
            print(f'size is set to {self._initial_size} -> {self.size()}')
            self._initial_size = QtCore.QSize(self.size().width() -30, self.size().height()-30)
            self._zoomed_size = QtCore.QSize(self.size().width() + 50, self.size().height()+50)
            self.updateAnimation(self.size(), self._zoomed_size)
            return super().paintEvent(a0)



class PushButton(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self._animation = QtCore.QPropertyAnimation(
            self, b"size",
            startValue=QtCore.QSize(100,80),
            endValue=QtCore.QSize(150,100),
            duration=400,
        )
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setMinimumSize(QtCore.QSize(100,80))
        
        

    def enterEvent(self, event):
        self._animation.setDirection(QtCore.QAbstractAnimation.Forward)
        self._animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._animation.setDirection(QtCore.QAbstractAnimation.Backward)
        self._animation.start()
        super().leaveEvent(event)

    


class Dialog(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle(self.tr("LWOLWSDf"))

        self.pushButton = PushButton()
        self.pushButton.setText(self.tr("Click Here"))
        self.pushButton.clicked.connect(self.getgraphsize)
    
        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self.pushButton, alignment=QtCore.Qt.AlignCenter)

        self.graphWidget = PGraph()
        hour = [1,2,3,4,5,6,7,8,9,10]
        temperature = [30,32,34,32,33,31,29,32,35,45]

        # plot data: x, y values
        self.graphWidget.plot(hour, temperature)
        lay.addWidget(self.graphWidget, alignment=QtCore.Qt.AlignCenter)
        print(self.graphWidget.sizeHint())
        self.resize(500, 350)

    def getgraphsize(self):
        print(f'size of graph is {self.graphWidget.size()}')


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = Dialog()
    w.show()
    sys.exit(app.exec_())