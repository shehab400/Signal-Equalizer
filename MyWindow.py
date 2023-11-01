from PyQt5 import QtWidgets, uic, QtCore
from pyqtgraph import PlotWidget, plot
from PyQt5.QtWidgets import (QApplication,QMainWindow,QVBoxLayout,QPushButton,QWidget,QErrorMessage,QMessageBox,QDialog,QScrollBar)
import simpleaudio as sa
import sys



class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("GUI.ui", self)
        self.actionLoad.triggered.connect(self.Load)
        self.actionStop.triggered.connect(self.Stop)
        self.play_obj = None

    def Load(self):
        filename = QtWidgets.QFileDialog.getOpenFileName()
        path = filename[0]
        wave_obj = sa.WaveObject.from_wave_file(path)
        self.play_obj = wave_obj.play()

    def Stop(self):
        if self.play_obj == None:
            return
        if self.play_obj.is_playing():
            self.play_obj.stop()