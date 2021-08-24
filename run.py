import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from app.Activitys.MainUI import MainUi
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('source/image/logo.png'))
    myWin = MainUi()
    myWin.show()
    sys.exit(app.exec_())