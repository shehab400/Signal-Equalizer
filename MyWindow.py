from PyQt5 import QtWidgets, uic, QtCore
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
from PyQt5.QtWidgets import (QApplication,QMainWindow,QVBoxLayout,QPushButton,QWidget,QErrorMessage,QMessageBox,QDialog,QScrollBar)
import simpleaudio as sa
import sys
from scipy.io.wavfile import read
from PlotLine import *
import sounddevice as sd
import soundfile as sf
import random
import time
from pydub import AudioSegment
from pydub.playback import play
from threading import *


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("GUI.ui", self)
        self.actionLoad.triggered.connect(self.Load)
        self.actionStop.triggered.connect(self.Stop)
        self.play_obj = None
        self.graphWidget1 = pg.PlotWidget()
        self.ui.gridLayout.addWidget(self.graphWidget1)
        self.newplot = None
        self.legend = self.graphWidget1.addLegend()
        self.timer = 0.0


    def Load(self):
        filename = QtWidgets.QFileDialog.getOpenFileName()
        path = filename[0]
        data, fs = sf.read(path, dtype='float32')
        self.newplot = PlotLine()
        self.newplot.name = filename[0]
        self.newplot.SetData(data,fs)
        self.newplot.data_line = self.graphWidget1.plot(self.newplot.time_axis,self.newplot.sound_axis,name=self.newplot.name)
        sd.play(data, fs)
        self.graphWidget1.setXRange(0,10,padding=0)
        self.timer1 = QtCore.QTimer()
        self.timer1.timeout.connect(self.update_plots)  # Connect to a single update method
        self.timer1.start(100)
        self.graphWidget1.setMouseEnabled(x=False,y=False)

    def random_color(self):
        red = random.randint(0,255)
        green = random.randint(0,255)
        blue = random.randint(0,255)
        return (red,green,blue)
    
    def update_plots(self):
        # random_rgb = self.random_color()
        # self.newplot.pen = pg.mkPen(color = random_rgb)
        # self.newplot.data_line.setPen(self.newplot.pen)
        self.timer += 0.126
        # xmin = self.graphWidget1.getViewBox().viewRange()[0][0]
        # xmax = self.graphWidget1.getViewBox().viewRange()[0][1]
        if self.timer > 10:
            self.graphWidget1.setXRange(self.timer-10, self.timer, padding=0)
        if self.timer > self.newplot.time_axis.max():
            self.timer1.stop()
            self.graphWidget1.setXRange(0,self.newplot.time_axis.max())


    def Stop(self):
        if self.play_obj == None:
            return
        if self.play_obj.is_playing():
            self.play_obj.stop()
        else:
            self.play_obj = None
    
    def Pause(self):
        pass