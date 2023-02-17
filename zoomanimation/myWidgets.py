from pyqtgraph import PlotWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot

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

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        if self._animation.state() == 2:
            return super().paintEvent(a0)
        elif self._animation.state() == 0 and not self._zoomed:
            # print(f'size is set to {self._initial_size} -> {self.size()}')
            self._initial_size = QtCore.QSize(self.size().width() -30, self.size().height()-30)
            self._zoomed_size = QtCore.QSize(self.size().width() + 50, self.size().height()+50)
            self.updateAnimation(self.size(), self._zoomed_size)
            return super().paintEvent(a0)

    def enterEvent(self, event): #TODO these must be on a thread. also there is a bug that makes it white
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

class AnimeThread(QtCore.QRunnable):
    '''
    Anime thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''
    def __init__(self, fn, *args, **kwargs):
        super(AnimeThread, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

        @pyqtSlot()
        def run(self):
            # apparently what this does it runs passed functions in separate threads
            self.fn(*self.args, *self.kwargs)


        

