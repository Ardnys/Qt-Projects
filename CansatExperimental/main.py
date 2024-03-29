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
        plot_list = [self.widget_ALTITUDE, self.widget_PRESSURE, self.widget_GPS_ALTITUDE, self.widget_TEMPERATURE, 
                       self.widget_VOLTAGE, self.widget_TILT_X, self.widget_TILT_Y]
        label_list = [self.altitude_last, self.pressure_last, self.GPS_altitude_last, self.temperature_last,
                      self.voltage_last, self.tilt_x_last, self.tilt_y_last]
        titles_list = ['Altitude (m)', 'Pressure (bar)', 'GPS_Altitude (m)', 'Temperature (°C)', 'Voltage (V)', 'Tilt_X (Degrees)', 'Tilt_Y (Degrees)']

        
        random_data = np.random.rand(7, 10)
        random_data *= 10
        # print(random_data)
        
        pen = pg.mkPen(color=((255, 211, 105)))
        styles = {'color':'#4DD599', 'font-family': "Chakra Petch Medium", 'font-size': '11px'}

        for (widget, data, label, description) in zip(plot_list, random_data, label_list, titles_list):
            widget.setBackground(("#393E46"))

            desc = description.split(' (')
            title, unit = desc[0].replace('_', ' '), desc[1]
            unit = unit.replace(')', '')
        
            widget.setTitle(title, color=((255, 211, 105)))
            widget.setLabel('left', description, **styles)
            widget.setLabel('bottom', 'Time (s)', **styles)
            widget.plot(seconds, data, pen=pen, symbol='o', symbolSize=7, symbolPen=((238, 238, 238)), symbolBrush=((77, 213, 153)))
            label.setText(str(round(data[-1], 3)) + ' ' + unit)
        
        long_random = np.random.rand(10)
        long_random *= 10
        lat_random = np.random.rand(10)
        lat_random *= 10
        self.widget_GPS_COORDINATES.setBackground(("#393E46"))
        self.widget_GPS_COORDINATES.setTitle('GPS Coordinates', color=((255, 211, 105)))
        self.widget_GPS_COORDINATES.setLabel('left', 'Longitude (Degrees)', **styles)
        self.widget_GPS_COORDINATES.setLabel('bottom', 'Latitude (Degrees)', **styles)
        self.widget_GPS_COORDINATES.plot(long_random, lat_random, pen=pen, symbol='x', symbolSize=7, symbolPen=((238, 238, 238)), symbolBrush=((77, 213, 153)))
        self.coordinates_last.setText(str(round(long_random[-1], 3)) + ' N ' + str(round(lat_random[-1], 3)) + ' W')

        for (long, lat) in zip(long_random, lat_random):
            self.telemetry_console.append('(' + str(round(long, 2)) + '), (' + str(round(lat, 2)) + ')')

        # self.telemetry_console.setFontFamily("Chakra Petch")

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