from PyQt5 import QtWidgets, uic, QtCore,QtGui,QtMultimedia
from PyQt5.QtCore import QThread,QObject,pyqtSignal as Signal, pyqtSlot as Slot
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
from PyQt5.QtWidgets import QApplication,QMainWindow,QVBoxLayout,QPushButton,QWidget,QErrorMessage,QMessageBox,QDialog,QScrollBar,QSlider
import simpleaudio as sa
import sys
from scipy.io.wavfile import read
import scipy
from PlotLine import *
import sounddevice as sd
import soundfile as sf
import random
import time
from pydub import AudioSegment
from pydub.playback import play
from threading import *
import numpy as np
import math
import audio2numpy as a2n
import pygame
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
from io import BytesIO
import pandas as pd
from InputDialog import *

windowSize = 1000
epsilon = 1e-10
gaussian_std = 5
x_axis = None
window = None

class Worker(QObject):
    progress = Signal(int)
    completed = Signal(int)
    end = False
    @Slot(int)
    def do_work(self, n):
        global i
        for i in np.arange(1,n+1,0.1):
            if self.end == True:
                break
            time.sleep(0.1)
            self.progress.emit(i)
        self.completed.emit(i)

class MyWindow(QMainWindow):
    work_requested = Signal(int)
    whichWindowing = None

    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = uic.loadUi("FixingGUI.ui", self)
        # self.ui = Ui_MainWindow()
        # self.ui.setupUi(self)
        self.setWindowTitle('Signal Equalizer')
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
        self.ui.playPauseSound.clicked.connect(self.Pause)
        self.ui.zoomIn.clicked.connect(self.ZoomIn)
        self.ui.zoomOut.clicked.connect(self.ZoomOut)
        self.ui.stop.clicked.connect(self.Stop)
        self.ui.reset.clicked.connect(self.Reset)
        self.ui.Rect.clicked.connect(self.rectFunc)
        self.ui.Hann.clicked.connect(self.hannFunc)
        self.ui.Hamm.clicked.connect(self.hammFunc)
        self.ui.Gauss.clicked.connect(self.gaussFunc)
        self.ui.cineSpeed.clicked.connect(self.SpeedControl)
 

        self.MediaPlayer = QMediaPlayer()
        self.worker = Worker()
        self.worker_thread = QThread()

        self.timePos = 0
        self.ZoomFactor = 0
        self.ispaused = False
       
        

        self.worker.progress.connect(self.UpdatePlots)
        self.worker.completed.connect(self.Complete)
        

        self.work_requested.connect(self.worker.do_work)

        # move worker to the worker thread
        self.worker.moveToThread(self.worker_thread)

        # start the thread
        self.worker_thread.start()

        #
        self.uniformSlider1 = self.findChild(QSlider, "verticalSlider")
        self.uniformSlider2 = self.findChild(QSlider, "verticalSlider_2")
        self.uniformSlider3 = self.findChild(QSlider, "verticalSlider_3")
        self.uniformSlider4 = self.findChild(QSlider, "verticalSlider_4")
        self.uniformSlider5 = self.findChild(QSlider, "verticalSlider_5")
        self.uniformSlider6 = self.findChild(QSlider, "verticalSlider_6")
        self.uniformSlider7 = self.findChild(QSlider, "verticalSlider_7")
        self.uniformSlider8 = self.findChild(QSlider, "verticalSlider_8")
        self.uniformSlider9 = self.findChild(QSlider, "verticalSlider_9")
        self.uniformSlider10 = self.findChild(QSlider, "verticalSlider_10")
        self.musicSlider1 = self.findChild(QSlider, "verticalSlider_11")
        self.musicSlider2 = self.findChild(QSlider, "verticalSlider_12")
        self.musicSlider3 = self.findChild(QSlider, "verticalSlider_13")
        self.musicSlider4 = self.findChild(QSlider, "verticalSlider_14")
        self.animalsSlider1 = self.findChild(QSlider, "verticalSlider_15")
        self.animalsSlider2 = self.findChild(QSlider, "verticalSlider_16")
        self.animalsSlider3 = self.findChild(QSlider, "verticalSlider_17")
        self.animalsSlider4 = self.findChild(QSlider, "verticalSlider_18")
        self.medicalSignalSlider1 = self.findChild(QSlider, "verticalSlider_19")
        self.medicalSignalSlider2 = self.findChild(QSlider, "verticalSlider_20")
        self.medicalSignalSlider3 = self.findChild(QSlider, "verticalSlider_21")
        self.medicalSignalSlider4 = self.findChild(QSlider, "verticalSlider_22")
        #
        self.ui.uniformSlider1.setMinimum(0)
        self.ui.uniformSlider2.setMinimum(0)
        self.ui.uniformSlider3.setMinimum(0)
        self.ui.uniformSlider4.setMinimum(0)
        self.ui.uniformSlider5.setMinimum(0)
        self.ui.uniformSlider6.setMinimum(0)
        self.ui.uniformSlider7.setMinimum(0)
        self.ui.uniformSlider8.setMinimum(0)
        self.ui.uniformSlider9.setMinimum(0)
        self.ui.uniformSlider10.setMinimum(0)
        self.ui.musicSlider1.setMinimum(0)
        self.ui.musicSlider2.setMinimum(0)
        self.ui.musicSlider3.setMinimum(0)
        self.ui.musicSlider4.setMinimum(0)
        self.ui.animalsSlider1.setMinimum(0)
        self.ui.animalsSlider2.setMinimum(0)
        self.ui.animalsSlider3.setMinimum(0)
        self.ui.animalsSlider4.setMinimum(0)
        self.ui.medicalSignalSlider1.setMinimum(0)
        self.ui.medicalSignalSlider2.setMinimum(0)
        self.ui.medicalSignalSlider3.setMinimum(0)
        self.ui.medicalSignalSlider4.setMinimum(0)
        #
        self.uniformSlider1.setMaximum(10)
        self.uniformSlider2.setMaximum(10)
        self.uniformSlider3.setMaximum(10)
        self.uniformSlider4.setMaximum(10)
        self.uniformSlider5.setMaximum(10)
        self.uniformSlider6.setMaximum(10)
        self.uniformSlider7.setMaximum(10)
        self.uniformSlider8.setMaximum(10)
        self.uniformSlider9.setMaximum(10)
        self.uniformSlider10.setMaximum(10)
        self.musicSlider1.setMaximum(10)
        self.musicSlider2.setMaximum(10)
        self.musicSlider3.setMaximum(10)
        self.musicSlider4.setMaximum(10)
        self.animalsSlider1.setMaximum(10)
        self.animalsSlider2.setMaximum(10)
        self.animalsSlider3.setMaximum(10)
        self.animalsSlider4.setMaximum(10)
        self.medicalSignalSlider1.setMaximum(10)
        self.medicalSignalSlider2.setMaximum(10)
        self.medicalSignalSlider3.setMaximum(10)
        self.medicalSignalSlider4.setMaximum(10)
        #
        self.uniformSlider1.setValue(5)
        self.uniformSlider2.setValue(5)
        self.uniformSlider3.setValue(5)
        self.uniformSlider4.setValue(5)
        self.uniformSlider5.setValue(5)
        self.uniformSlider6.setValue(5)
        self.uniformSlider7.setValue(5)
        self.uniformSlider8.setValue(5)
        self.uniformSlider9.setValue(5)
        self.uniformSlider10.setValue(5)
        self.musicSlider1.setValue(5)
        self.musicSlider2.setValue(5)
        self.musicSlider3.setValue(5)
        self.musicSlider4.setValue(5)
        self.animalsSlider1.setValue(5)
        self.animalsSlider2.setValue(5)
        self.animalsSlider3.setValue(5)
        self.animalsSlider4.setValue(5)
        self.medicalSignalSlider1.setValue(5)
        self.medicalSignalSlider2.setValue(5)
        self.medicalSignalSlider3.setValue(5)
        self.medicalSignalSlider4.setValue(5)

        #
        self.uniformSlider1.setTickPosition(QSlider.TicksLeft)
        self.uniformSlider2.setTickPosition(QSlider.TicksLeft)
        self.uniformSlider3.setTickPosition(QSlider.TicksLeft)
        self.uniformSlider4.setTickPosition(QSlider.TicksLeft)
        self.uniformSlider5.setTickPosition(QSlider.TicksLeft)
        self.uniformSlider6.setTickPosition(QSlider.TicksLeft)
        self.uniformSlider7.setTickPosition(QSlider.TicksLeft)
        self.uniformSlider8.setTickPosition(QSlider.TicksLeft)
        self.uniformSlider9.setTickPosition(QSlider.TicksLeft)
        self.uniformSlider10.setTickPosition(QSlider.TicksLeft)
        self.musicSlider1.setTickPosition(QSlider.TicksLeft)
        self.musicSlider2.setTickPosition(QSlider.TicksLeft)
        self.musicSlider3.setTickPosition(QSlider.TicksLeft)
        self.musicSlider4.setTickPosition(QSlider.TicksLeft)
        self.animalsSlider1.setTickPosition(QSlider.TicksLeft)
        self.animalsSlider2.setTickPosition(QSlider.TicksLeft)
        self.animalsSlider3.setTickPosition(QSlider.TicksLeft)
        self.animalsSlider4.setTickPosition(QSlider.TicksLeft)
        self.medicalSignalSlider1.setTickPosition(QSlider.TicksLeft)
        self.medicalSignalSlider2.setTickPosition(QSlider.TicksLeft)
        self.medicalSignalSlider3.setTickPosition(QSlider.TicksLeft)
        self.medicalSignalSlider4.setTickPosition(QSlider.TicksLeft)
        # connect sliders to the function
        for slider in [self.musicSlider1,self.musicSlider2,self.musicSlider3,self.musicSlider4]:
            slider.valueChanged.connect(self.update_frequency_components)
        for slider in [self.animalsSlider1,self.animalsSlider2,self.animalsSlider3,self.animalsSlider4]:
            slider.valueChanged.connect(self.update_frequency_components)
        for slider in [self.uniformSlider1, self.uniformSlider2, self.uniformSlider3, self.uniformSlider4,self.uniformSlider5, self.uniformSlider6, self.uniformSlider7, self.uniformSlider8,self.uniformSlider9, self.uniformSlider10]:
            slider.valueChanged.connect(self.update_frequency_components)
        for slider in [self.medicalSignalSlider1, self.medicalSignalSlider2, self.medicalSignalSlider3, self.medicalSignalSlider4]:
            slider.valueChanged.connect(self.arrhythmiaRemoval)
        #
        self.plotWidget1 = pg.PlotWidget()
        self.plotWidget2 = pg.PlotWidget()
        self.plotWidget3 = pg.PlotWidget()
        self.plotWidget4 = pg.PlotWidget()
        self.plotWidget5 = pg.PlotWidget()
        self.plotWidget6 = pg.PlotWidget()
         # Create Matplotlib figure and axes
        self.matplotlib_figure, self.matplotlib_axes = plt.subplots()
        self.matplotlib_axes.set_axis_off()  # Turn off axes for spectrogram

        # Create Matplotlib widget to embed in PyQT layout
        self.matplotlib_widget = FigureCanvasQTAgg(self.matplotlib_figure)
        self.matplotlib_axes.set_facecolor('black')
        self.matplotlib_figure.patch.set_facecolor('black')
        ####
        self.matplotlib_figure2, self.matplotlib_axes2 = plt.subplots()
        self.matplotlib_axes2.set_axis_off()  # Turn off axes for spectrogram

        # Create Matplotlib widget to embed in PyQT layout
        self.matplotlib_widget2 = FigureCanvasQTAgg(self.matplotlib_figure)
        self.matplotlib_axes2.set_facecolor('black')
        self.matplotlib_figure2.patch.set_facecolor('black')

        # Add Matplotlib widget to the layout
        # self.ui.verticalLayout.addWidget(self.matplotlib_widget)
        layout1=QVBoxLayout()
        layout1.addWidget(self.plotWidget1 )
        self.ui.widget_2.setLayout(layout1)
        layout2=QVBoxLayout()
        layout2.addWidget(self.matplotlib_widget)
        self.ui.widget_4.setLayout(layout2)
        layout3=QVBoxLayout()
        layout3.addWidget(self.plotWidget3)
        self.ui.widget_5.setLayout(layout3)
        layout4=QVBoxLayout()
        layout4.addWidget(self.plotWidget4 )
        self.ui.widget_6.setLayout(layout4)
        layout5=QVBoxLayout()
        layout5.addWidget(self.matplotlib_widget2 )
        self.ui.widget_7.setLayout(layout5)
        layout6=QVBoxLayout()
        layout6.addWidget(self.plotWidget6 )
        self.ui.widget_8.setLayout(layout6)

        self.plotWidget1.setMouseEnabled(x=True, y=False)
        self.plotWidget4.setMouseEnabled(x=True, y=False)

    def rectFunc(self):
        self.whichWindowing = 1
        window = np.ones(windowSize)
        x_axis = np.arange(windowSize)
        self.plotWidget6.clear()
        self.plotWidget6.plot( x_axis, window, title='Rectangular Smoothing Window')
        
    def hannFunc(self):
        self.whichWindowing = 2 
        window = np.hanning(windowSize)
        x = np.arange(windowSize)
        self.plotWidget6.clear()
        self.plotWidget6.plot( x, window, title='Rectangular Smoothing Window')

    def hammFunc(self):
        self.whichWindowing = 3 
        window = np.hamming(windowSize)
        x = np.arange(windowSize)
        self.plotWidget6.clear()
        self.plotWidget6.plot( x, window, title='Rectangular Smoothing Window')

    def gaussFunc(self):
        self.whichWindowing = 4
        window = np.exp(-(0.5 * ((windowSize - 1) / 2 - np.arange(windowSize)) / (gaussian_std * (windowSize -1)/2))**2)
        x = np.arange(windowSize)
        self.plotWidget6.clear()
        self.plotWidget6.plot( x, window, title='Rectangular Smoothing Window')
        
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

    def UpdateAudio(self,time_axis,sound_axis,fs):
        pos = self.MediaPlayer.position()
        self.MediaPlayer.stop()
        self.MediaPlayer = QMediaPlayer()
        data = np.array(list(zip(time_axis,sound_axis)))
        sf.write("test.wav",data,fs)
        sound = AudioSegment.from_wav("test.wav")
        os.remove('test.wav')
        sound = sound.set_channels(1)
        if os.path.exists('test.mp3'):
            os.remove("test.mp3")
        sound.export("test.mp3", format="mp3")
        self.timePos += pos
        url = QtCore.QUrl.fromLocalFile("test.mp3")
        self.MediaPlayer.setMedia(QtMultimedia.QMediaContent(url))
        self.MediaPlayer.setPosition(pos)
        self.MediaPlayer.play()

    def Load(self):
        if self.ui.stackedWidget.currentIndex() == 1 or self.ui.stackedWidget.currentIndex() == 2:
            #Load filee, Plot, Convert Every track to frequency, get frequency ranges, update plot
            filename = QtWidgets.QFileDialog.getOpenFileName()
            path = filename[0]
            data, fs = a2n.audio_from_file(path)

            self.input = PlotLine()
            self.input.name = path
            self.input.fs=fs
            self.input.SetData(data,fs)
            #self.SetFrequencyRanges(path)
            self.plotWidget1.clear()
            self.input.data_line = self.plotWidget1.plot(self.input.time_axis,self.input.sound_axis,name=self.input.name)
            self.plotWidget1.setLimits(xMin = 0 ,xMax = self.input.time_axis.max())
            self.generate_spectrogram(self.input.time_axis,self.input.sound_axis,self.input.fs,1)
            self.update_frequency_components()
            self.generate_spectrogram(self.input.time_axis,self.input.sound_axis,self.input.fs,2)
            self.timePos = 0
            # pygame.mixer.music.unload()
            # pygame.mixer.music.load(path)
            # pygame.mixer.music.play()
            
            url = QtCore.QUrl.fromLocalFile(path)
            self.MediaPlayer.setMedia(QtMultimedia.QMediaContent(url))
            self.MediaPlayer.play()
            #self.MediaPlayer.stateChanged.connect(self.Completed)

            self.plotWidget1.setXRange(0,10,padding=0)

            self.work_requested.emit(300)

        elif self.ui.stackedWidget.currentIndex() == 0:
            #Load filee, Plot, Convert Every track to frequency, get frequency ranges, update plot
            filename = QtWidgets.QFileDialog.getOpenFileName()
            path = filename[0]
            data, fs = a2n.audio_from_file(path)
            
            self.input = PlotLine()
            self.input.name = path
            self.input.fs=fs
            self.input.SetData(data,fs)
            self.plotWidget1.clear()
            self.input.data_line = self.plotWidget1.plot(self.input.time_axis,self.input.sound_axis,name=self.input.name)
            self.plotWidget1.setLimits(xMin = 0 ,xMax = self.input.time_axis.max())
            self.generate_spectrogram(self.input.time_axis,self.input.sound_axis,self.input.fs,1)
            self.update_frequency_components()

            # pygame.mixer.music.load(path)
            # pygame.mixer.music.play()

            self.plotWidget1.setXRange(0,10,padding=0)

            self.work_requested.emit(300)
        elif self.ui.stackedWidget.currentIndex() == 3: 
            filename = QtWidgets.QFileDialog.getOpenFileName()
            path = filename[0]
            self.input = PlotLine()
            if path=="C:/projects/DSP/Task 3/Signal-Equalizer/used arrhythemia signals/rec_1.dat":
                self.input.arrhythmiaType=1
            elif path=="C:/projects/DSP/Task 3/Signal-Equalizer/used arrhythemia signals/rec_3.dat":
                self.input.arrhythmiaType=2
            elif path=="C:/projects/DSP/Task 3/Signal-Equalizer/used arrhythemia signals/rec_2.dat":
                self.input.arrhythmiaType=3
            elif path=="C:/projects/DSP/Task 3/Signal-Equalizer/used arrhythemia signals/rec_4.dat":
                self.input.arrhythmiaType=4
                
            print(path)
            with open(path, 'rb') as file:
                # Read binary data
                binary_data = file.read()
                
                # Convert binary data to a 1D array of integers
                values2= np.frombuffer(binary_data, dtype=np.int32)
                data1=values2.copy()
                values=data1[:9000]
                
               #fs is already known in medical signals
                fs = 500.0  # Sample rate in Hz
                
                # Calculate time values
                time_values = np.arange(0, len(values) / fs, 1 / fs)
            path1="C:/projects/DSP/Task 3/Signal-Equalizer/arrhythmia signals/rec_1.dat"
            with open(path1,'rb') as file1:
                data=file1.read()
            # normal_ecg=pd.read_csv(path1, usecols=["time", "amplitude"])
            normal_ecg=np.frombuffer(data, dtype=np.int32)
            # data1=normal_ecg1.copy()
            # normal_ecg=data1[:10000]
            uniform_fft = np.fft.fft(normal_ecg)
            # print(uniform_fft)
            self.input.uniform_fft=uniform_fft
            self.input.uniform_fftfreq = np.fft.fftfreq(len(uniform_fft), 1/500)
            self.input.name = path
            self.input.fs=fs
            self.input.time_axis=time_values
            self.input.sound_axis=values
           
            self.input.fft = np.fft.fft(values)
            # Calculate the frequency axis
            fs = 500.0  # fs for any medical signal from physionet 
            self.input.FrequencySamples = np.fft.fftfreq(len(values), 1/fs)
            self.plotWidget1.clear()
            self.input.data_line = self.plotWidget1.plot(self.input.time_axis,self.input.sound_axis,name=self.input.name)
            self.generate_spectrogram(self.input.time_axis,self.input.sound_axis,self.input.fs,1)
            self.plotWidget1.setXRange(0,10,padding=0)
            # self.update_frequency_components()
            self.arrhythmiaRemoval()
            self.work_requested.emit(300)

    
    def ZoomIn(self):
        if self.ZoomFactor > -9:
            self.ZoomFactor -= 1
        
    def ZoomOut(self):
        self.ZoomFactor += 1

    def Pause(self):
        if self.ispaused == False:
            self.MediaPlayer.pause()
            self.ispaused = True
        elif self.ispaused == True:
            self.MediaPlayer.play()
            self.ispaused = False

    def Stop(self):
        self.MediaPlayer.stop()
        self.ispaused = True

    def Reset(self):
        sliders = [self.uniformSlider1,self.uniformSlider2,self.uniformSlider3,self.uniformSlider4,self.uniformSlider5,self.uniformSlider6,self.uniformSlider7,self.uniformSlider8,self.uniformSlider9,self.uniformSlider10,
                   self.musicSlider1,self.musicSlider2,self.musicSlider3,self.musicSlider4,
                   self.animalsSlider1,self.animalsSlider2,self.animalsSlider3,self.animalsSlider4,
                   self.medicalSignalSlider1,self.medicalSignalSlider2,self.medicalSignalSlider3,self.medicalSignalSlider4]
        for slider in sliders:
            slider.setValue(5)

    def SpeedControl(self):
        dialog = InputDialog(self)
        result = dialog.exec_()  # This will block until the user closes the dialog

        if result == QtWidgets.QDialog.Accepted:
            user_input = dialog.input_text.text()
            # Do something with the user input, e.g., display it in a message box
            self.MediaPlayer.setPlaybackRate(float(user_input))

    # def Rewind(self):
    #     if self.ui.stackedWidget.currentIndex() == 1 or self.ui.stackedWidget.currentIndex() == 2:
    #         pygame.mixer.music.rewind()
    #     elif self.ui.stackedWidget.currentIndex() == 0 or self.ui.stackedWidget.currentIndex() == 3:
    #         self.plotWidget1.setXRange(0,10,padding=0)
    #         self.plotWidget4.setXRange(0,10,padding=0)

    # def SetFrequencyRanges(self,filename):
    #     if self.ui.stackedWidget.currentIndex() == 1:
    #         self.Bass = self.Drums = self.Keyboard = self.Guitar = PlotLine()
    #         self.Bass.name = filename.replace(".mp3","") + " - Bass.mp3"
    #         self.Drums.name = filename.replace(".mp3","") + " - Drums.mp3"
    #         self.Keyboard.name = filename.replace(".mp3","") + " - Keyboard.mp3"
    #         self.Guitar.name = filename.replace(".mp3","") + " - Guitar.mp3"
    #         list = [self.Bass,self.Drums,self.Keyboard,self.Guitar]
    #         for plot in list:
    #             data, fs = a2n.audio_from_file(plot.name)
    #             plot.fs=fs
    #             plot.SetData(data,fs)

    # def UpdateComposed(self):
    #     data, fs = a2n.audio_from_file("ComposedSound.mp3")
        
    #     self.input = PlotLine()
    #     self.input.name = "ComposedSound"
    #     self.input.fs=fs
    #     self.input.SetData(data,fs)
    #     self.plotWidget1.clear()
    #     self.input.data_line = self.plotWidget1.plot(self.input.time_axis,self.input.sound_axis,name=self.input.name)

    # def KeyboardAdjustor(self):
    #     if self.sounds != None:
    #         NewSound = self.sounds[0] + ((self.musicSlider1.value()-5)*2)
    #         pos = pygame.mixer.music.get_pos()
    #         self.timePos += pos
    #         pygame.mixer.music.unload()
    #         if os.path.exists('ComposedSound.mp3'):
    #             os.remove("ComposedSound.mp3")
    #         self.SoundMerge(NewSound,self.sounds[1],self.sounds[2],self.sounds[3])
    #         self.UpdateComposed()
    #         pygame.mixer.music.load("ComposedSound.mp3")
    #         pygame.mixer.music.play()
    #         pygame.mixer.music.rewind() # mp3 files need a rewind first
    #         pygame.mixer.music.set_pos(self.timePos/1000)

    def random_color(self):
        red = random.randint(0,255)
        green = random.randint(0,255)
        blue = random.randint(0,255)
        
        return (red,green,blue)
    

    def UpdatePlots(self):
        # random_rgb = self.random_color()
        # self.input.pen = pg.mkPen(color = random_rgb)
        # self.input.data_line.setPen(self.input.pen)
        if self.ispaused == False:
            if self.ui.stackedWidget.currentIndex() == 0 or self.ui.stackedWidget.currentIndex() == 3:
                    xmin=self.plotWidget1.getViewBox().viewRange()[0][0]
                    xmax=self.plotWidget1.getViewBox().viewRange()[0][1]
                    self.plotWidget1.setXRange(xmin+0.1,xmax+0.1+self.ZoomFactor,padding=0)
                    self.plotWidget4.setXRange(xmin+0.1,xmax+0.1+self.ZoomFactor,padding=0)
            
            elif self.ui.stackedWidget.currentIndex() == 1 or self.ui.stackedWidget.currentIndex() == 2:
                self.plotWidget1.setXRange((self.MediaPlayer.position()/1000), (self.MediaPlayer.position()/1000)+10+self.ZoomFactor, padding=0)
                self.plotWidget4.setXRange((self.MediaPlayer.position()/1000), (self.MediaPlayer.position()/1000)+10+self.ZoomFactor, padding=0)
            #self.timePos = pygame.mixer.get_pos()/1000

    def Completed(self):
        self.plotWidget1.setXRange(0,self.input.time_axis.max())
        self.plotWidget4.setXRange(0,self.input.time_axis.max())

    def Complete(self):
        pass
        
    def generate_spectrogram(self, time_axis, sound_axis, fs,flag):
        if flag==1:
            Pxx, frequencies, times, img = self.matplotlib_axes.specgram(sound_axis, Fs=fs, cmap='viridis', NFFT=256, noverlap=128)
            # Draw the Matplotlib figure
            self.matplotlib_widget.draw()
            # Clear the existing content in the Matplotlib figure
            # self.matplotlib_figure.canvas.clf()
            # Plot the spectrogram in the Matplotlib figure
            self.matplotlib_axes.pcolormesh(times, frequencies, 10 * np.log10(Pxx), shading='auto', cmap='viridis')
            self.matplotlib_axes.set_xlabel('Time (s)')
            self.matplotlib_axes.set_ylabel('Frequency (Hz)')
            self.matplotlib_axes.set_title('Spectrogram')
        if flag==2:
            Pxx, frequencies, times, img = self.matplotlib_axes2.specgram(sound_axis, Fs=fs, cmap='viridis', NFFT=256, noverlap=128)
            # Draw the Matplotlib figure
            self.matplotlib_widget2.draw()
            # Clear the existing content in the Matplotlib figure
            self.matplotlib_axes2.clear()
            # Plot the spectrogram in the Matplotlib figure
            self.matplotlib_axes2.pcolormesh(times, frequencies, 10 * np.log10(Pxx), shading='auto', cmap='viridis')
            self.matplotlib_axes2.set_xlabel('Time (s)')
            self.matplotlib_axes2.set_ylabel('Frequency (Hz)')
            self.matplotlib_axes2.set_title('Spectrogram')
        # Update the colorbar
        if hasattr(self.matplotlib_axes2, 'get_images') and len(self.matplotlib_axes2.get_images()) > 0:
            self.matplotlib_figure.colorbar(self.matplotlib_axes2.get_images()[0], ax=self.matplotlib_axes2)
    
    def update_frequency_components(self):
        if self.ui.stackedWidget.currentIndex() == 1:
            original_spectrum = self.input.fft
            frequency_axis = self.input.FrequencySamples
            positive_freq_indices = np.where(frequency_axis > 0)
            Sliders = [self.musicSlider1,self.musicSlider2,self.musicSlider3,self.musicSlider4]
            frequency_ranges = [(300,1000),(900,3000),(0,300),(2000,10000)] #Piano,Guitar,Bass,Flute
            modified_spectrum = np.copy(original_spectrum)

            for slider, (freq_min, freq_max) in zip(Sliders, frequency_ranges):
                amplification_factor = slider.value() * 0.2

                # Find the indices of the frequency range
                pos_indices = np.where((frequency_axis >= freq_min) & (frequency_axis <= freq_max))
                neg_indices = np.where((frequency_axis >= -freq_max) & (frequency_axis <= -freq_min))
                # Adjust the magnitude in the frequency domain
                modified_spectrum[pos_indices] *= amplification_factor
                modified_spectrum[neg_indices] *= amplification_factor
            
            # frequency_ranges = [(-100,0),(-250,-100),(-1200,-300),(-4186,-1200)]   
            # for slider, (freq_min, freq_max) in zip(Sliders, frequency_ranges):
            #     amplification_factor = slider.value() * 0.2

            #     indices = np.where((frequency_axis >= freq_min) & (frequency_axis <= freq_max))
            #     # Adjust the magnitude in the frequency domain
            #     modified_spectrum[indices] *= amplification_factor
            self.plotFrequencyDomain(frequency_axis,modified_spectrum,positive_freq_indices)

            # Compute the inverse Fourier Transform to get the modified signal
            modified_signal = np.fft.ifft(modified_spectrum).real

            # Update the plot with the modified signal in the time domain
            self.plotWidget4.clear()
            self.input.data_line = self.plotWidget4.plot(self.input.time_axis, modified_signal, name=self.input.name)
            self.plotWidget4.setLimits(xMin = 0,xMax = self.input.time_axis.max())
            self.generate_spectrogram(self.input.time_axis,modified_signal,self.input.fs,2)
            self.UpdateAudio(self.input.time_axis,modified_signal,self.input.fs)
            self.plotWidget3.setLabel('left', 'Amplitude')
            self.plotWidget3.setLabel('bottom', 'Frequency (Hz)')

        elif self.ui.stackedWidget.currentIndex() == 2:
            original_spectrum = self.input.fft
            frequency_axis = self.input.FrequencySamples
            positive_freq_indices = np.where(frequency_axis > 0)
            signal_min_freq = frequency_axis[positive_freq_indices].min()
            signal_max_freq = frequency_axis[positive_freq_indices].max()
            Sliders = [self.animalsSlider1,self.animalsSlider2,self.animalsSlider3,self.animalsSlider4]
            frequency_ranges = [(10,700), (700,1600) , (1500,2500) , (2500 ,7000)] #lion, elephant cat dog
            # frequency_ranges = [(10,1400),(1400,2500),(2500,4000),(4000,11000)] #lion, elephant cat dog
            modified_spectrum = np.copy(original_spectrum)

            for slider, (freq_min, freq_max) in zip(Sliders, frequency_ranges):
                amplification_factor = slider.value() * 0.2

                # Find the indices of the frequency range
                indices = np.where((frequency_axis >= freq_min) & (frequency_axis <= freq_max))

                # Adjust the magnitude in the frequency domain
                modified_spectrum[indices] *= amplification_factor
            
            frequency_ranges = [(-700,-10),(-1600,-700),(-2500,-1500),(-7000,-2500)] #lion, elephant cat dog           
            # frequency_ranges = [(-1400,-10),(-2500,-1400),(-4000,-2500) , (-11000,-4000)] #lion, elephant cat dog           
            for slider, (freq_min, freq_max) in zip(Sliders, frequency_ranges):
                amplification_factor = slider.value() * 0.2

                indices = np.where((frequency_axis >= freq_min) & (frequency_axis <= freq_max))
                # Adjust the magnitude in the frequency domain
                modified_spectrum[indices] *= amplification_factor
            self.plotFrequencyDomain(frequency_axis,modified_spectrum,positive_freq_indices)

            # Compute the inverse Fourier Transform to get the modified signal
            modified_signal = np.fft.ifft(modified_spectrum).real

            # Update the plot with the modified signal in the time domain
            self.plotWidget4.clear()
            self.input.data_line = self.plotWidget4.plot(self.input.time_axis, modified_signal, name=self.input.name)
            self.plotWidget4.setLimits(xMin = 0,xMax = self.input.time_axis.max())
            self.generate_spectrogram(self.input.time_axis,modified_signal,self.input.fs,2)
            self.UpdateAudio(self.input.time_axis,modified_signal,self.input.fs)
            self.plotWidget3.setLabel('left', 'Amplitude')
            self.plotWidget3.setLabel('bottom', 'Frequency (Hz)')

        elif self.ui.stackedWidget.currentIndex() == 0:
            # Compute the Fourier Transform for the original signal
            # original_spectrum = np.fft.fft(self.input.sound_axis)
            original_spectrum=self.input.fft
            frequency_axis=self.input.FrequencySamples

            # # Calculate the frequency resolution and create the frequency axis
            # time_step = 1.0 / self.input.fs
            # frequency_axis = np.fft.fftfreq(len(self.input.sound_axis), time_step)
             # Initialize an array for the modified spectrum    
            modified_spectrum = np.copy(original_spectrum)
            # Find the positive frequencies (ignore negative frequencies)
            positive_freq_indices = np.where(frequency_axis > 0)

            # Get the minimum and maximum frequencies
            signal_min_freq = frequency_axis[positive_freq_indices].min()
            signal_max_freq = frequency_axis[positive_freq_indices].max()

            # Get the slider values
            uniform_sliders = [
                self.uniformSlider1, self.uniformSlider2, self.uniformSlider3, self.uniformSlider4,
                self.uniformSlider5, self.uniformSlider6, self.uniformSlider7, self.uniformSlider8,
                self.uniformSlider9, self.uniformSlider10
            ]

            # Calculate the frequency range for each slider based on the loaded signal's range
            frequency_ranges = [
                (
                    signal_min_freq + i * (signal_max_freq - signal_min_freq) / 10,
                    signal_min_freq + (i + 1) * (signal_max_freq - signal_min_freq) / 10
                ) for i in range(10)
            ]

           
            

            # Adjust the magnitudes based on the slider values, with increased amplification
            for slider, (freq_min, freq_max) in zip(uniform_sliders, frequency_ranges):
                amplification_factor = slider.value() / 10.0  # Normalize the slider value to [0, 1]
                amplitude = amplification_factor * 2  # Square the amplitude for increased effect

                # Find the indices of the frequency range
                indices = np.where((frequency_axis >= freq_min) & (frequency_axis <= freq_max))

                # Adjust the magnitude in the frequency domain
                modified_spectrum[indices] *= amplitude

            # Update the plot with the original signal and the modified signal in the frequency domain
            # self.plotWidget2.clear()
            # self.plotWidget2.plot(
            #     frequency_axis[positive_freq_indices],
            #     np.abs(original_spectrum[positive_freq_indices]),
            #     pen='b',
            #     name='Original Spectrum'
            # )
            # self.plotWidget2.setLabel('left', 'Amplitude')
            # self.plotWidget2.setLabel('bottom', 'Frequency (Hz)')

            # self.plotWidget3.clear()
            # self.plotWidget3.plot(
            #     frequency_axis[positive_freq_indices],
            #     np.abs(modified_spectrum[positive_freq_indices]),
            #     pen='r',
            #     name='Modified Spectrum'
            # )
            self.plotFrequencyDomain(frequency_axis,modified_spectrum,positive_freq_indices)

            # Compute the inverse Fourier Transform to get the modified signal
            modified_signal = np.fft.ifft(modified_spectrum).real

            # Update the plot with the modified signal in the time domain
            self.plotWidget4.clear()
            self.input.data_line = self.plotWidget4.plot(self.input.time_axis, modified_signal, name=self.input.name)
            self.plotWidget4.setLimits(xMin = 0,xMax = self.input.time_axis.max())
            self.generate_spectrogram(self.input.time_axis,modified_signal,self.input.fs,2)
            # self.plotWidget4.setXRange(0, self.input.time_axis.max())
            self.plotWidget3.setLabel('left', 'Amplitude')
            self.plotWidget3.setLabel('bottom', 'Frequency (Hz)')
        
    def plotFrequencyDomain(self,frequency_axis,modified_spectrum,positive_freq_indices):
        if self.whichWindowing == None:
            self.plotWidget3.clear()
            self.plotWidget3.plot(
                frequency_axis[positive_freq_indices],
                np.abs(modified_spectrum[positive_freq_indices]),
                pen='r',
                name='Modified Spectrum'
            )
        if self.whichWindowing == 1:
            modified_spectrum[positive_freq_indices] *= np.ones(len(positive_freq_indices))
            self.plotWidget3.clear()
            self.plotWidget3.plot(
                frequency_axis[positive_freq_indices],
                np.abs(modified_spectrum[positive_freq_indices]),
                pen='r',
                name='Modified Spectrum'
            )
        if self.whichWindowing == 2:
            # Apply Hanning windowing using np.hann
            modified_spectrum[positive_freq_indices] *= np.hanning(len(positive_freq_indices))
            self.plotWidget3.clear()
            self.plotWidget3.plot(
                frequency_axis[positive_freq_indices],
                np.abs(modified_spectrum[positive_freq_indices]),
                pen='r',
                name='Modified Spectrum'
            )
        if self.whichWindowing == 3:
            modified_spectrum[positive_freq_indices] *= np.hamming(len(positive_freq_indices))
            self.plotWidget3.clear()
            self.plotWidget3.plot(
                frequency_axis[positive_freq_indices],
                np.abs(modified_spectrum[positive_freq_indices]),
                pen='r',
                name='Modified Spectrum'
            )
        if self.whichWindowing == 4:
            modified_spectrum[positive_freq_indices] *= np.exp(-(0.5 * ((len(positive_freq_indices) - 1) / 2 - np.arange(len(positive_freq_indices))) / (gaussian_std * (len(positive_freq_indices) -1)/2 ))**2)
            self.plotWidget3.clear()
            self.plotWidget3.plot(
                frequency_axis[positive_freq_indices],
                np.abs(modified_spectrum[positive_freq_indices]),
                pen='r',
                name='Modified Spectrum'
            )

    def arrhythmiaRemoval(self):
        original_spectrum = self.input.fft
        modified_spectrum = original_spectrum.copy()  # Make a copy to avoid modifying the original
        positive_freq_indices = np.where(self.input.FrequencySamples > 0)
        positive_freq_indices2 = np.where(self.input.uniform_fftfreq > 0)

        # Get the slider values
        medical_sliders = [
            self.medicalSignalSlider1, self.medicalSignalSlider2, self.medicalSignalSlider3
        ]

        # Calculate the arrhythmia frequencies
        arythmia_freq = set(self.input.FrequencySamples[positive_freq_indices]) - set(self.input.uniform_fftfreq[positive_freq_indices2])
        # print(arythmia_freq)
        arythmia_freq = np.array(list(arythmia_freq)) 
        # print(len(self.input.FrequencySamples[positive_freq_indices]))
        # print(len(original_spectrum[positive_freq_indices]))
        # print(len(self.input.uniform_fft[positive_freq_indices2]))
        # Get the magnitude difference for each frequency
        # magnitude_difference = np.abs(original_spectrum[positive_freq_indices] - self.input.uniform_fft[positive_freq_indices2])

        # # Sort frequencies based on magnitude difference
        # sorted_indices = np.argsort(magnitude_difference)[::-1]

        # # Select the top frequencies
        # top_frequencies = self.input.FrequencySamples[positive_freq_indices][sorted_indices]

        # # Get the indices corresponding to the top frequencies
        # top_indices = positive_freq_indices[0][sorted_indices[:2000]]

        # # Print or use the top frequencies and indices as needed
        # print("Top Important Frequencies:", top_frequencies)
        # print("Top Important Frequencies Indices:", top_indices)

          # Find the indices of arrhythmia frequencies in the frequency array
        # indices = np.where(np.isin(self.input.FrequencySamples[positive_freq_indices], list(arythmia_freq)))
        # indices = np.where((self.input.FrequencySamples[positive_freq_indices] >= 30) & (self.input.FrequencySamples[positive_freq_indices] <= 180))
        print(self.input.arrhythmiaType)
        if self.input.arrhythmiaType==1:
            freq_min=0
            freq_max=69
            amplification_factor = self.medicalSignalSlider1.value() / 10.0  # Normalize the slider value to [0, 1]
            if self.medicalSignalSlider1.value()!=5:
                amplitude = amplification_factor * 2  # Square the amplitude for increased effect
                # modified_spectrum[top_indices] *= amplitude
                indices = np.where((arythmia_freq >= freq_min) & (arythmia_freq <= freq_max))
                modified_spectrum[indices] *= amplitude
                
            
        if self.input.arrhythmiaType==2:
            freq_min=70
            freq_max=140
            amplification_factor = self.medicalSignalSlider2.value() / 10.0  # Normalize the slider value to [0, 1]
            if self.medicalSignalSlider2.value()!=5:
                amplitude = amplification_factor * 2  # Square the amplitude for increased effect
                # modified_spectrum[top_indices] *= amplitude
                indices = np.where((arythmia_freq >= freq_min) & (arythmia_freq <= freq_max))
                modified_spectrum[indices] *= amplitude
        if self.input.arrhythmiaType==3:
            freq_min=140
            freq_max=200
            amplification_factor = self.medicalSignalSlider3.value() / 10.0  # Normalize the slider value to [0, 1]
            if self.medicalSignalSlider3.value()!=5:
                amplitude = amplification_factor * 2  # Square the amplitude for increased effect
                # modified_spectrum[top_indices] *= amplitude
                indices = np.where((arythmia_freq >= freq_min) & (arythmia_freq <= freq_max))
                modified_spectrum[indices] *= amplitude
        if self.input.arrhythmiaType==4:
            freq_min=200
            freq_max=260
            amplification_factor = self.medicalSignalSlider4.value() / 10.0  # Normalize the slider value to [0, 1]
            if self.medicalSignalSlider4.value()!=5:
                amplitude = amplification_factor * 2  # Square the amplitude for increased effect
                # modified_spectrum[top_indices] *= amplitude
                indices = np.where((arythmia_freq >= freq_min) & (arythmia_freq <= freq_max))
                modified_spectrum[indices] *= amplitude
                    
        # frequency_Ranges=[(0,80),(90,150),(160,260)]
        # for slider , (freq_min, freq_max) in  zip (medical_sliders,frequency_Ranges):
        #     amplification_factor = slider.value() / 10.0  # Normalize the slider value to [0, 1]
        #     if slider.value()!=5:
        #         amplitude = amplification_factor * 2  # Square the amplitude for increased effect
        #         # modified_spectrum[top_indices] *= amplitude
        #         indices = np.where((arythmia_freq >= freq_min) & (arythmia_freq <= freq_max))
        #         modified_spectrum[indices] *= amplitude

        self.plotFrequencyDomain(self.input.FrequencySamples, modified_spectrum, positive_freq_indices)
        # Compute the inverse Fourier Transform to get the modified signal
        modified_signal = np.fft.ifft(modified_spectrum).real

        # Update the plot with the modified signal in the time domain
        self.plotWidget4.clear()
        self.input.data_line = self.plotWidget4.plot(
            self.input.time_axis, modified_signal, name=self.input.name
        )
        self.generate_spectrogram(self.input.time_axis,modified_signal,self.input.fs,2)

