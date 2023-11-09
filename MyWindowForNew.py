from PyQt5 import QtWidgets, uic, QtCore
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
from PyQt5.QtWidgets import (QApplication,QMainWindow,QVBoxLayout,QPushButton,QWidget,QErrorMessage,QMessageBox,QDialog,QScrollBar,QSlider)
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
        self.ui = uic.loadUi("FixingGUI.ui", self)
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
        self.ui.actionLoad.clicked.connect(self.Load)
        #
        self.unifromSlider1 = self.findChild(QSlider, "verticalSlider_1")
        self.unifromSlider2 = self.findChild(QSlider, "verticalSlider_2")
        self.unifromSlider3 = self.findChild(QSlider, "verticalSlider_3")
        self.unifromSlider4 = self.findChild(QSlider, "verticalSlider_4")
        self.unifromSlider5 = self.findChild(QSlider, "verticalSlider_5")
        self.unifromSlider6 = self.findChild(QSlider, "verticalSlider_6")
        self.unifromSlider7 = self.findChild(QSlider, "verticalSlider_7")
        self.unifromSlider8 = self.findChild(QSlider, "verticalSlider_8")
        self.unifromSlider9 = self.findChild(QSlider, "verticalSlider_9")
        self.unifromSlider10 = self.findChild(QSlider, "verticalSlider_10")
        #
        # self.ui.unifromSlider1.setMinimum(0)
        # self.ui.unifromSlider2.setMinimum(0)
        # self.ui.unifromSlider3.setMinimum(0)
        # self.ui.unifromSlider4.setMinimum(0)
        # self.ui.unifromSlider5.setMinimum(0)
        # self.ui.unifromSlider6.setMinimum(0)
        # self.ui.unifromSlider7.setMinimum(0)
        # self.ui.unifromSlider8.setMinimum(0)
        # self.ui.unifromSlider9.setMinimum(0)
        # self.ui.unifromSlider10.setMinimum(0)
        # #
        # self.unifromSlider1.setMaximum(10)
        # self.unifromSlider2.setMaximum(10)
        # self.unifromSlider3.setMaximum(10)
        # self.unifromSlider4.setMaximum(10)
        # self.unifromSlider5.setMaximum(10)
        # self.unifromSlider6.setMaximum(10)
        # self.unifromSlider7.setMaximum(10)
        # self.unifromSlider8.setMaximum(10)
        # self.unifromSlider9.setMaximum(10)
        # self.unifromSlider10.setMaximum(10)
        # #
        # self.unifromSlider1.setValue(5)
        # self.unifromSlider2.setValue(5)
        # self.unifromSlider3.setValue(5)
        # self.unifromSlider4.setValue(5)
        # self.unifromSlider5.setValue(5)
        # self.unifromSlider6.setValue(5)
        # self.unifromSlider7.setValue(5)
        # self.unifromSlider8.setValue(5)
        # self.unifromSlider9.setValue(5)
        # self.unifromSlider10.setValue(5)
        # #

        self.plotWidget1 = pg.PlotWidget()
        self.plotWidget2 = pg.PlotWidget()
        self.plotWidget3 = pg.PlotWidget()
        self.plotWidget4 = pg.PlotWidget()
        self.plotWidget5 = pg.PlotWidget()
        self.plotWidget6 = pg.PlotWidget()

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
        self.ui.widget_8.setLayout(layout6)
        
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
        self.ui.stackedWidget_2.setCurrentIndex(0)

    def uniformWave_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.stackedWidget_2.setCurrentIndex(0)

    def music_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.stackedWidget_2.setCurrentIndex(1)

    def music_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.stackedWidget_2.setCurrentIndex(1)

    def animals_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        self.ui.stackedWidget_2.setCurrentIndex(2)

    def animals_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        self.ui.stackedWidget_2.setCurrentIndex(2)

    def medicalSignal_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(3)
        self.ui.stackedWidget_2.setCurrentIndex(3)

    def medicalSignal_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(3)
        self.ui.stackedWidget_2.setCurrentIndex(3)

    def Load(self):
        pass
