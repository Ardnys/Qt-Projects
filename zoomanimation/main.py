from PyQt5.QtWidgets import QWidget, QPushButton, QMainWindow
from PyQt5.QtCore import QPropertyAnimation, QPoint, QEasingCurve, QSize
from PyQt5 import QtWidgets, uic
import pyqtgraph as pg
import sys
import resources

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('customgraphtest.ui', self)
        hour = [1,2,3,4,5,6,7,8,9,10]
        temperature = [30,32,34,32,33,31,29,32,35,45]
        widget_list = [self.plotwidget_1, self.plotwidget_2, self.plotwidget_3, self.plotwidget_4, 
                       self.plotwidget_5, self.plotwidget_6, self.plotwidget_7, self.plotwidget_8]
        
        pen = pg.mkPen(color=((255, 211, 105)))

        for widget in widget_list:
            widget.setBackground(("#393E46"))
            widget.setTitle("amazing graphs", color=((255, 211, 105)))
            styles = {'color':'#4DD599', 'font-family': "Chakra Petch Medium", 'font-size': '11px'}
            widget.setLabel('left', 'Temperature (°C)', **styles)
            widget.setLabel('bottom', 'Hour (H)', **styles)
            widget.plot(hour, temperature, pen=pen, symbol='o', symbolSize=7, symbolPen=((238, 238, 238)), symbolBrush=((77, 213, 153)))

        # self.plotwidget_1.setBackground(("#393E46"))
        # self.plotwidget_2.setBackground(("#393E46"))
        # self.plotwidget_3.setBackground(("#393E46"))
        # self.plotwidget_4.setBackground(("#393E46"))
        # self.plotwidget_5.setBackground(("#393E46"))
        # self.plotwidget_6.setBackground(("#393E46"))
        # self.plotwidget_7.setBackground(("#393E46"))
        # self.plotwidget_8.setBackground(("#393E46"))

        # self.plotwidget_1.plot(hour, temperature, pen=pen)
        # self.plotwidget_2.plot(hour, temperature, pen=pen)
        # self.plotwidget_3.plot(hour, temperature, pen=pen)
        # self.plotwidget_4.plot(hour, temperature, pen=pen)
        # self.plotwidget_5.plot(hour, temperature, pen=pen)
        # self.plotwidget_6.plot(hour, temperature, pen=pen)
        # self.plotwidget_7.plot(hour, temperature, pen=pen)
        # self.plotwidget_8.plot(hour, temperature, pen=pen)

        

        

    

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    thing = Window()
    thing.show()
    sys.exit(app.exec_())