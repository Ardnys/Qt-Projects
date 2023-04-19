from PyQt5 import QtCore, QtGui, QtWidgets, uic
import pyqtgraph as pg
import sys
import numpy as np


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('cansatexperimentalgui.ui', self)
        self.showMaximized()

        seconds = [1,2,3,4,5,6,7,8,9,10]
        temperature = [30,32,34,32,33,31,29,32,35,45]
        plot_list = [self.widget_ALTITUDE, self.widget_PRESSURE, self.widget_GPS_ALTITUDE, self.widget_TEMPERATURE, 
                       self.widget_VOLTAGE, self.widget_TILT_X, self.widget_TILT_Y]
        
        random_data = np.random.rand(7, 10)
        random_data *= 10
        # print(random_data)
        
        pen = pg.mkPen(color=((255, 211, 105)))

        for (widget, data) in zip(plot_list, random_data):
            widget.setBackground(("#393E46"))
            # widget.setTitle("amazing graphs", color=((255, 211, 105)))
            styles = {'color':'#4DD599', 'font-family': "Chakra Petch Medium", 'font-size': '11px'}
            # widget.setLabel('left', 'Temperature (°C)', **styles)
            # widget.setLabel('bottom', 'Hour (H)', **styles)
            widget.plot(seconds, data, pen=pen, symbol='o', symbolSize=7, symbolPen=((238, 238, 238)), symbolBrush=((77, 213, 153)))
        
        self.widget_ALTITUDE.setTitle("Altitude", color=((255, 211, 105)))
        self.widget_PRESSURE.setTitle("Pressure", color=((255, 211, 105)))
        self.widget_GPS_ALTITUDE.setTitle("GPS Altitude", color=((255, 211, 105)))
        self.widget_TEMPERATURE.setTitle("Temperature", color=((255, 211, 105)))
        self.widget_VOLTAGE.setTitle("Voltage", color=((255, 211, 105)))
        self.widget_TILT_X.setTitle("Tilt X", color=((255, 211, 105)))
        self.widget_TILT_Y.setTitle("Tilt Y", color=((255, 211, 105)))

        self.widget_ALTITUDE.setLabel('left', 'Altitude (m)', **styles)
        self.widget_PRESSURE.setLabel('left', 'Pressure ()', **styles)
        self.widget_GPS_ALTITUDE.setLabel('left', 'Altitude (m)', **styles)
        self.widget_TEMPERATURE.setLabel('left', 'Temperature (°C)', **styles)
        self.widget_VOLTAGE.setLabel('left', 'Voltage (V)', **styles)
        self.widget_TILT_X.setLabel('left', 'Tilt (Degrees)', **styles)
        self.widget_TILT_Y.setLabel('left', 'Tilt (Degrees)', **styles)

        self.widget_ALTITUDE.setLabel('bottom', 'Time (s)', **styles)
        self.widget_PRESSURE.setLabel('bottom', 'Time (s)', **styles)
        self.widget_GPS_ALTITUDE.setLabel('bottom', 'Time (s)', **styles)
        self.widget_TEMPERATURE.setLabel('bottom', 'Time (s)', **styles)
        self.widget_VOLTAGE.setLabel('bottom', 'Time (s)', **styles)
        self.widget_TILT_X.setLabel('bottom', 'Time (s)', **styles)
        self.widget_TILT_Y.setLabel('bottom', 'Time (s)', **styles)

        widget.setLabel('left', 'Temperature (°C)', **styles)
        widget.setLabel('bottom', 'Hour (H)', **styles)

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