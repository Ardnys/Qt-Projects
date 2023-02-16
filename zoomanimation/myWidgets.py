from pyqtgraph import PlotWidget
from PyQt5 import QtCore, QtGui, QtWidgets

class GraphWidget(PlotWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._initial_size = self.size()
        self._zoomed = False
        self._animation = QtCore.QPropertyAnimation(
            self, b"size",
            startValue=self._initial_size,
            endValue=QtCore.QSize(self._initial_size.width()+10, self._initial_size.height()+10),
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
        self._zoomed = True
        self.raise_()
        self._animation.setDirection(QtCore.QAbstractAnimation.Forward)
        self._animation.start()
        super().enterEvent(event)
        

    def leaveEvent(self, event):
        self._animation.setDirection(QtCore.QAbstractAnimation.Backward)
        self._animation.start()
        super().leaveEvent(event)
        self._zoomed = False
        
        

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        if self._animation.state() == 2:
            return super().paintEvent(a0)
        elif self._animation.state() == 0 and not self._zoomed:
            # print(f'size is set to {self._initial_size} -> {self.size()}')
            self._initial_size = QtCore.QSize(self.size().width() -30, self.size().height()-30)
            self._zoomed_size = QtCore.QSize(self.size().width() + 50, self.size().height()+50)
            self.updateAnimation(self.size(), self._zoomed_size)
            return super().paintEvent(a0)

