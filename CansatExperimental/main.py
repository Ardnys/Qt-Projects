from PyQt5 import QtCore, QtGui, QtWidgets, uic
import pyqtgraph as pg
import sys


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('cansatexperimentalgui.ui', self)
        self.showMaximized()

        hour = [1,2,3,4,5,6,7,8,9,10]
        temperature = [30,32,34,32,33,31,29,32,35,45]
        plot_list = [self.widget_ALTITUDE, self.widget_PRESSURE, self.widget_GPS_ALTITUDE, self.widget_TEMPERATURE, 
                       self.widget_VOLTAGE, self.widget_TILT_X, self.widget_TILT_Y]
        
        pen = pg.mkPen(color=((255, 211, 105)))

        for widget in plot_list:
            widget.setBackground(("#393E46"))
            widget.setTitle("amazing graphs", color=((255, 211, 105)))
            styles = {'color':'#4DD599', 'font-family': "Chakra Petch Medium", 'font-size': '11px'}
            widget.setLabel('left', 'Temperature (°C)', **styles)
            widget.setLabel('bottom', 'Hour (H)', **styles)
            widget.plot(hour, temperature, pen=pen, symbol='o', symbolSize=7, symbolPen=((238, 238, 238)), symbolBrush=((77, 213, 153)))

        logo_pixmap = QtGui.QPixmap('canbeelogosmall.jpg')
        self.team_logo.setPixmap(logo_pixmap)
        self.team_logo.resize(100, 100)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dir_ = QtCore.QDir("ChakraPetch")
    QtGui.QFontDatabase.addApplicationFont("ChakraPetch/ChakraPetch-Medium.ttf")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())