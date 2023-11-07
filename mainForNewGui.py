import sys
from PyQt5.QtWidgets import (QApplication,QMainWindow)
from PyQt5.QtCore import pyqtSlot, QFile, QTextStream

from NEW_GUI import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.icon_only.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.unifromWave.setChecked(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())