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


class _BatteryDisplay(QtWidgets.QWidget):
    """
    It has a segmented display like old phone battery indicators
    colors and spacing can be customised"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding
        )

        self.value = 100
    
    def updateValue(self, voltage: float):
        # update battery juice here
        # connect this function 
        self.value = voltage
        self.update()

    
    def sizeHint(self):
        return QtCore.QSize(200,60)
    
    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        try:
            # just a black rectangle
            painter = QtGui.QPainter(self)
            brush = QtGui.QBrush()
            brush.setColor(QtGui.QColor(238, 238, 238))
            brush.setStyle(QtCore.Qt.SolidPattern)
            background_path = QtGui.QPainterPath()
            background_path.addRoundedRect(QtCore.QRectF(0, 0, int(painter.device().width()*0.95), int(painter.device().height())), 10, 10)
            battip = QtGui.QPainterPath()
            battip.setFillRule(QtCore.Qt.WindingFill)
            battip.addRoundedRect(QtCore.QRectF(painter.device().width()*0.95, painter.device().height()*.3, painter.device().width()*0.05, painter.device().height()*0.4), 7, 7)
            battip.addRect(QtCore.QRectF(
                painter.device().width()*0.95,
                painter.device().height()*.3,
                painter.device().width()*0.025,
                painter.device().height()*0.4
            ))
                        
            painter.fillPath(battip, brush)
            brush.setColor(QtGui.QColor('black'))
            painter.fillPath(background_path, brush)

            painter.setPen(QtGui.QPen(QtGui.QColor(238, 238, 238)))
            # painter.drawRect(QtCore.QRect(0, 0, int(painter.device().width()*0.95), int(painter.device().height() * 0.999)))

            border_path = QtGui.QPainterPath()
            border_path.addRoundedRect(0, 0, int(painter.device().width()*0.95), int(painter.device().height()*.99), 15, 15)
            painter.drawPath(border_path)


            label = self.parent().label

            vmin = 0
            vmax = 100
            padding = 5

            # Define our canvas.
            d_height = painter.device().height() - (padding * 2)
            d_width = int(painter.device().width()*0.95 - (padding * 2))

            # Draw the bars.
            boi = 10
            step_size = d_width / boi
            bar_width = step_size 
        
            pc = (self.value - vmin) / (vmax - vmin)
            n_steps_to_draw = int(pc * boi)
            brush.setColor(QtGui.QColor('lime'))
            for n in range(boi, boi-n_steps_to_draw, -1):
                path = QtGui.QPainterPath()
                path.setFillRule(QtCore.Qt.WindingFill)
                if n == 10:
                    # left is not rounded
                    rect = QtCore.QRectF(
                            padding + d_width - ((n) * step_size),
                            padding,
                            bar_width,
                            d_height
                        )
                    path.addRect(QtCore.QRectF(
                        (padding + d_width - ((n) * step_size))*3,
                        padding,
                        bar_width/2,
                        d_height
                    ))
                    path.addRoundedRect(rect, 10, 10)
                elif n == 1:
                    # right is not rounded
                    rect = QtCore.QRectF(
                            padding + d_width - ((n) * step_size),
                            padding,
                            bar_width,
                            d_height
                        )
                    path.addRect(QtCore.QRectF(
                        padding + d_width - ((n) * step_size),
                        padding,
                        bar_width/2,
                        d_height
                    ))
                    path.addRoundedRect(rect, 10, 10)
                else: 
                    path.addRect(QtCore.QRectF(
                        padding + d_width - ((n) * step_size),
                        padding,
                        bar_width,
                        d_height
                    ))
                painter.fillPath(path, brush)
                

            label.setText(str(self.value) + " %")

            painter.end()
        except Exception as e:
            print("error while painting battery " + str(e))


class BatteryIndicator(QtWidgets.QWidget):
    """
    This is just for testing the functionality of BatteryDisplay
    I change the value with a button and it shows the changes in the display
    We won't need it when we make sure the display works
    oh mY PKCELL!!!
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # LCD shows the bat percentage
        layout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel()
        self.label.setStyleSheet('color:rgb(25, 255, 25);background-color:rgb(0, 0, 0)')
        
        # self._lcd = QtWidgets.QLCDNumber()
        # self._lcd.setDigitCount(3)
        # self._lcd.setStyleSheet('color:rgb(25, 255, 25);background-color:rgb(0, 0, 0)')
        # self._lcd.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        layout.addWidget(self.label, 1)

        # displays juice
        self._bar = _BatteryDisplay()
        layout.addWidget(self._bar, 3)
        self.setLayout(layout)
        # self.setStyleSheet('background: rgb(255,255,255);')

    def UpdateBattery(self, voltage: float):
        self._bar.updateValue(float(voltage))
        

