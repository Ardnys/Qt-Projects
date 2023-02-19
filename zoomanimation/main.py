from PyQt5.QtWidgets import QWidget, QPushButton, QMainWindow
from PyQt5.QtCore import QPropertyAnimation, QPoint, QEasingCurve, QSize
from PyQt5 import QtWidgets, uic

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('customgraphtest.ui', self)
        # self.resize(600, 600)
        # self.child = QPushButton(self)
        # # self.child.setStyleSheet("background-color:red;border-radius:15px;")
        # self.child.resize(100, 100)
        # self.child.move(QPoint(200,200))
        # self.anim = QPropertyAnimation(self.child, b"size")
        # self.anim.setEasingCurve(QEasingCurve.InOutCubic)
        # self.anim.setEndValue(QSize(200, 200))
        # self.anim.setDuration(750)
        # self.child.clicked.connect(self.anim.start)
        hour = [1,2,3,4,5,6,7,8,9,10]
        temperature = [30,32,34,32,33,31,29,32,35,45]
        self.plotwidget.plot(hour, temperature)

    

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    thing = Window()
    thing.show()
    sys.exit(app.exec_())