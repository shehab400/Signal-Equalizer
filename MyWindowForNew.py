from PyQt5 import QtWidgets, uic, QtCore
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
from PyQt5.QtWidgets import (QApplication,QMainWindow,QVBoxLayout,QPushButton,QWidget,QErrorMessage,QMessageBox,QDialog,QScrollBar)
import simpleaudio as sa
import sys
from scipy.io.wavfile import read
from PlotLine import *
# import sounddevice as sd
# import soundfile as sf
import random
import time
# from pydub import AudioSegment
# from pydub.playback import play
from threading import *


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = uic.loadUi("GUI.ui", self)
        # self.ui = Ui_MainWindow()
        # self.ui.setupUi(self)
        self.ui.icon_only.hide()
        self.ui.uniformWave.clicked.connect(self.uniformWave_1_toggled)
        self.ui.music.clicked.connect(self.music_1_toggled)
        self.ui.animals.clicked.connect(self.animals_1_toggled)
        self.ui.medicalSignal.clicked.connect(self.medicalSignal_1_toggled)
        self.ui.uniformWave2.clicked.connect(self.uniformWave_2_toggled)
        self.ui.music2.clicked.connect(self.music_2_toggled)
        self.ui.animals2.clicked.connect(self.animals_2_toggled)
        self.ui.medicalSignal2.clicked.connect(self.medicalSignal_2_toggled)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.uniformWave.setChecked(True)
        self.plotWidget1 = pg.PlotWidget()
        self.plotWidget2 = pg.PlotWidget()
        self.plotWidget3 = pg.PlotWidget()
        self.plotWidget4 = pg.PlotWidget()
        self.plotWidget5 = pg.PlotWidget()
        self.plotWidget6 = pg.PlotWidget()
        self.plotWidget7 = pg.PlotWidget()
        self.plotWidget8 = pg.PlotWidget()
        self.plotWidget9 = pg.PlotWidget()
        self.plotWidget10 = pg.PlotWidget()
        self.plotWidget11 = pg.PlotWidget()
        self.plotWidget12 = pg.PlotWidget()
        self.plotWidget13 = pg.PlotWidget()
        self.plotWidget14 = pg.PlotWidget()
        self.plotWidget15 = pg.PlotWidget()
        self.plotWidget16 = pg.PlotWidget()
        self.plotWidget17 = pg.PlotWidget()
        self.plotWidget18 = pg.PlotWidget()
        self.plotWidget19 = pg.PlotWidget()
        self.plotWidget20 = pg.PlotWidget()

        layout1=QVBoxLayout()
        layout1.addWidget(self.plotWidget1 )
        self.ui.widget_2.setLayout(layout1)
        layout2=QVBoxLayout()
        layout2.addWidget(self.plotWidget2 )
        self.ui.widget_4.setLayout(layout2)
        layout3=QVBoxLayout()
        layout3.addWidget(self.plotWidget3 )
        self.ui.widget_5.setLayout(layout3)
        layout4=QVBoxLayout()
        layout4.addWidget(self.plotWidget4 )
        self.ui.widget_6.setLayout(layout4)
        layout5=QVBoxLayout()
        layout5.addWidget(self.plotWidget5 )
        self.ui.widget_7.setLayout(layout5)
        layout6=QVBoxLayout()
        layout6.addWidget(self.plotWidget6 )
        self.ui.widget_10.setLayout(layout6)
        layout7=QVBoxLayout()
        layout7.addWidget(self.plotWidget7 )
        self.ui.widget_11.setLayout(layout7)
        layout8=QVBoxLayout()
        layout8.addWidget(self.plotWidget8 )
        self.ui.widget_12.setLayout(layout8)
        layout9=QVBoxLayout()
        layout9.addWidget(self.plotWidget9 )
        self.ui.widget_13.setLayout(layout9)
        layout10=QVBoxLayout()
        layout10.addWidget(self.plotWidget10 )
        self.ui.widget_14.setLayout(layout10)
        ###
        layout11=QVBoxLayout()
        layout11.addWidget(self.plotWidget11 )
        self.ui.widget_25.setLayout(layout11)
        layout12=QVBoxLayout()
        layout12.addWidget(self.plotWidget12 )
        self.ui.widget_27.setLayout(layout12)
        layout13=QVBoxLayout()
        layout13.addWidget(self.plotWidget13 )
        self.ui.widget_19.setLayout(layout13)
        layout14=QVBoxLayout()
        layout14.addWidget(self.plotWidget14 )
        self.ui.widget_24.setLayout(layout14)
        layout15=QVBoxLayout()
        layout15.addWidget(self.plotWidget15 )
        self.ui.widget_26.setLayout(layout15)
        layout16=QVBoxLayout()
        layout16.addWidget(self.plotWidget16 )
        self.ui.widget_17.setLayout(layout16)
        layout17=QVBoxLayout()
        layout17.addWidget(self.plotWidget17 )
        self.ui.widget_18.setLayout(layout17)
        layout18=QVBoxLayout()
        layout18.addWidget(self.plotWidget18 )
        self.ui.widget_20.setLayout(layout18)
        layout19=QVBoxLayout()
        layout19.addWidget(self.plotWidget19 )
        self.ui.widget_21.setLayout(layout19)
        layout20=QVBoxLayout()
        layout20.addWidget(self.plotWidget20 )
        self.ui.widget_28.setLayout(layout20)



## Change Qpushbutton Checkable status when stackedWidget index changed  
    def stackedWidget_currentChanged (self, index):
        btn_list = self.ui.icon_only.findChild(QPushButton) \
        + self.ui.full_menu.findChild(QPushButton)

        for btn in btn_list:
            if index in [5,6]:
                btn.setAutoExclusive(False)
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)

    def uniformWave_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def uniformWave_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def music_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def music_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def animals_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def animals_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def medicalSignal_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def medicalSignal_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(3)

