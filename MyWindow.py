from PyQt5 import QtWidgets, uic, QtCore,QtGui
from PyQt5.QtCore import QThread,QObject,pyqtSignal as Signal, pyqtSlot as Slot
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


class Worker(QObject):
    progress = Signal(int)
    completed = Signal(int)
    @Slot(int)
    def do_work(self, n):
        global i
        for i in np.arange(1,n+1,0.1):
            time.sleep(0.1)
            self.progress.emit(i)
        self.completed.emit(i)

class MyWindow(QMainWindow):
    work_requested = Signal(int)

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

        pygame.mixer.init()
        self.worker = Worker()
        self.worker_thread = QThread()

        self.timePos = 0
        self.sounds = None

        self.worker.progress.connect(self.UpdatePlots)
        self.worker.completed.connect(self.Complete)
        

        self.work_requested.connect(self.worker.do_work)

        # move worker to the worker thread
        self.worker.moveToThread(self.worker_thread)

        # start the thread
        self.worker_thread.start()

        #
        self.unifromSlider1 = self.findChild(QSlider, "verticalSlider")
        self.unifromSlider2 = self.findChild(QSlider, "verticalSlider_2")
        self.unifromSlider3 = self.findChild(QSlider, "verticalSlider_3")
        self.unifromSlider4 = self.findChild(QSlider, "verticalSlider_4")
        self.unifromSlider5 = self.findChild(QSlider, "verticalSlider_5")
        self.unifromSlider6 = self.findChild(QSlider, "verticalSlider_6")
        self.unifromSlider7 = self.findChild(QSlider, "verticalSlider_7")
        self.unifromSlider8 = self.findChild(QSlider, "verticalSlider_8")
        self.unifromSlider9 = self.findChild(QSlider, "verticalSlider_9")
        self.unifromSlider10 = self.findChild(QSlider, "verticalSlider_10")
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
        self.ui.unifromSlider1.setMinimum(0)
        self.ui.unifromSlider2.setMinimum(0)
        self.ui.unifromSlider3.setMinimum(0)
        self.ui.unifromSlider4.setMinimum(0)
        self.ui.unifromSlider5.setMinimum(0)
        self.ui.unifromSlider6.setMinimum(0)
        self.ui.unifromSlider7.setMinimum(0)
        self.ui.unifromSlider8.setMinimum(0)
        self.ui.unifromSlider9.setMinimum(0)
        self.ui.unifromSlider10.setMinimum(0)
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
        self.unifromSlider1.setMaximum(10)
        self.unifromSlider2.setMaximum(10)
        self.unifromSlider3.setMaximum(10)
        self.unifromSlider4.setMaximum(10)
        self.unifromSlider5.setMaximum(10)
        self.unifromSlider6.setMaximum(10)
        self.unifromSlider7.setMaximum(10)
        self.unifromSlider8.setMaximum(10)
        self.unifromSlider9.setMaximum(10)
        self.unifromSlider10.setMaximum(10)
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
        self.unifromSlider1.setValue(5)
        self.unifromSlider2.setValue(5)
        self.unifromSlider3.setValue(5)
        self.unifromSlider4.setValue(5)
        self.unifromSlider5.setValue(5)
        self.unifromSlider6.setValue(5)
        self.unifromSlider7.setValue(5)
        self.unifromSlider8.setValue(5)
        self.unifromSlider9.setValue(5)
        self.unifromSlider10.setValue(5)
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
        self.ui.verticalSlider_11.valueChanged.connect(self.update_frequency_components)
        self.ui.verticalSlider_12.valueChanged.connect(self.update_frequency_components)
        self.ui.verticalSlider_13.valueChanged.connect(self.update_frequency_components)
        self.ui.verticalSlider_14.valueChanged.connect(self.update_frequency_components)
        self.ui.verticalSlider_15.valueChanged.connect(self.update_frequency_components)
        self.ui.verticalSlider_16.valueChanged.connect(self.update_frequency_components)
        self.ui.verticalSlider_17.valueChanged.connect(self.update_frequency_components)
        self.ui.verticalSlider_18.valueChanged.connect(self.update_frequency_components)

        #
        self.unifromSlider1.setTickPosition(QSlider.TicksLeft)
        self.unifromSlider2.setTickPosition(QSlider.TicksLeft)
        self.unifromSlider3.setTickPosition(QSlider.TicksLeft)
        self.unifromSlider4.setTickPosition(QSlider.TicksLeft)
        self.unifromSlider5.setTickPosition(QSlider.TicksLeft)
        self.unifromSlider6.setTickPosition(QSlider.TicksLeft)
        self.unifromSlider7.setTickPosition(QSlider.TicksLeft)
        self.unifromSlider8.setTickPosition(QSlider.TicksLeft)
        self.unifromSlider9.setTickPosition(QSlider.TicksLeft)
        self.unifromSlider10.setTickPosition(QSlider.TicksLeft)
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
        # connect uniform sliders to the uniform function
        for slider in [
            self.unifromSlider1, self.unifromSlider2, self.unifromSlider3, self.unifromSlider4,
            self.unifromSlider5, self.unifromSlider6, self.unifromSlider7, self.unifromSlider8,
            self.unifromSlider9, self.unifromSlider10
        ]:
            slider.valueChanged.connect(self.update_frequency_components)
             # connect medical sliders to the arythmia function
        for slider in [
            self.medicalSignalSlider1, self.medicalSignalSlider2, self.medicalSignalSlider3, self.medicalSignalSlider4
        ]:
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

        self.plotWidget1.setMouseEnabled(x=False,y=False)
        self.plotWidget4.setMouseEnabled(x=False, y=False)
        
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
        data = np.array(list(zip(time_axis,sound_axis)))
        sf.write("test.wav",data,fs)
        sound = AudioSegment.from_wav("test.wav")
        os.remove('test.wav')
        sound = sound.set_channels(1)
        pygame.mixer.music.unload()
        if os.path.exists('test.mp3'):
            os.remove("test.mp3")
        sound.export("test.mp3", format="mp3")
        pos = pygame.mixer.music.get_pos()
        self.timePos += pos
        pygame.mixer.music.load("test.mp3")
        pygame.mixer.music.play()
        pygame.mixer.music.rewind() # mp3 files need a rewind first
        pygame.mixer.music.set_pos(self.timePos/1000)

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
            self.generate_spectrogram(self.input.time_axis,self.input.sound_axis,self.input.fs,1)
            self.update_frequency_components()
            self.generate_spectrogram(self.input.time_axis,self.input.sound_axis,self.input.fs,2)

            pygame.mixer.music.load(path)
            pygame.mixer.music.play()

            self.plotWidget1.setXRange(0,10,padding=0)

            self.work_requested.emit(math.ceil(self.input.time_axis.max()))

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
            self.generate_spectrogram(self.input.time_axis,self.input.sound_axis,self.input.fs,1)
            self.update_frequency_components()

            # pygame.mixer.music.load(path)
            # pygame.mixer.music.play()

            self.plotWidget1.setXRange(0,10,padding=0)

            self.work_requested.emit(math.ceil(self.input.time_axis.max()))
        elif self.ui.stackedWidget.currentIndex() == 3: 
            filename = QtWidgets.QFileDialog.getOpenFileName()
            path = filename[0]
            with open(path, 'rb') as file:
                # Read binary data
                binary_data = file.read()
                
                # Convert binary data to a 1D array of integers
                values = np.frombuffer(binary_data, dtype=np.int64)
                
               #fs is already known in medical signals
                fs = 500.0  # Sample rate in Hz
                
                # Calculate time values
                time_values = np.arange(0, len(values) / fs, 1 / fs)
            path1="C:/projects/DSP/Task 3/Signal-Equalizer/arrhythmia signals/ECG.csv"
            normal_ecg=pd.read_csv(path1, usecols=["time", "amplitude"])
            uniform_fft = np.fft.fft(normal_ecg['amplitude'])
            self.input = PlotLine()
            self.input.uniform_fftfreq = np.fft.fftfreq(len(uniform_fft), 1/2)
            self.input.name = path
            self.input.fs=fs
            self.input.time_axis=time_values
            self.input.sound_axis=values
            signal = np.frombuffer(self.input.sound_axis, dtype=np.int64)
            # Determine the number of rows (adjust as needed based on your data)
            num_rows = len(signal) // 2
            # Reshape the 1D array to a 2D array
            signal_2d = signal.reshape((num_rows, -1))
            # Extract the desired column
            column_data = signal_2d[:, 1]
            # Compute the FFT on the extracted column
            self.input.fft = np.fft.fft(column_data)
            # Calculate the frequency axis
            fs = 500.0  # fs for any medical signal from physionet 
            self.input.FrequencySamples = np.fft.fftfreq(len(column_data), 1/fs)
            self.plotWidget1.clear()
            self.input.data_line = self.plotWidget1.plot(self.input.time_axis,self.input.sound_axis,name=self.input.name)
            self.generate_spectrogram(self.input.time_axis,self.input.sound_axis,self.input.fs,1)
            self.plotWidget1.setXRange(0,10,padding=0)
            # self.update_frequency_components()
            self.arrhythmiaRemoval()
            self.work_requested.emit(math.ceil(self.input.time_axis.max()))

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

    def UpdateComposed(self):
        data, fs = a2n.audio_from_file("ComposedSound.mp3")
        
        self.input = PlotLine()
        self.input.name = "ComposedSound"
        self.input.fs=fs
        self.input.SetData(data,fs)
        self.plotWidget1.clear()
        self.input.data_line = self.plotWidget1.plot(self.input.time_axis,self.input.sound_axis,name=self.input.name)

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
        if self.ui.stackedWidget.currentIndex() == 0 or self.ui.stackedWidget.currentIndex() == 3:
            xmin=self.plotWidget1.getViewBox().viewRange()[0][0]
            xmax=self.plotWidget1.getViewBox().viewRange()[0][1]
            self.plotWidget1.setXRange(xmin+0.1,xmax+0.1,padding=0)
            self.plotWidget4.setXRange(xmin+0.1,xmax+0.1,padding=0)
        
        elif self.ui.stackedWidget.currentIndex() == 1 or self.ui.stackedWidget.currentIndex() == 2:
           self.plotWidget1.setXRange((self.timePos+pygame.mixer.music.get_pos())/1000, ((self.timePos+pygame.mixer.music.get_pos())/1000)+10, padding=0)
           self.plotWidget4.setXRange((self.timePos+pygame.mixer.music.get_pos())/1000, ((self.timePos+pygame.mixer.music.get_pos())/1000)+10, padding=0)
        #self.timePos = pygame.mixer.get_pos()/1000

    def Complete(self):
        self.plotWidget1.setXRange(0,self.input.time_axis.max())
        
    def generate_spectrogram(self, time_axis, sound_axis, fs,flag):
        if flag==1:
            Pxx, frequencies, times, img = self.matplotlib_axes.specgram(sound_axis, Fs=fs, cmap='viridis', NFFT=256, noverlap=128)
            # Draw the Matplotlib figure
            self.matplotlib_widget.draw()
            # Clear the existing content in the Matplotlib figure
            self.matplotlib_axes.clear()
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
            self.input.data_line = self.plotWidget4.plot(
                self.input.time_axis, modified_signal, name=self.input.name
            )
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
            frequency_ranges = [(200,2500), (2500,20000) , (0,0) , (0 ,0)] #lion, elephant cat dog
            # frequency_ranges = [(10,1400),(1400,2500),(2500,4000),(4000,11000)] #lion, elephant cat dog
            modified_spectrum = np.copy(original_spectrum)

            for slider, (freq_min, freq_max) in zip(Sliders, frequency_ranges):
                amplification_factor = slider.value() * 0.2

                # Find the indices of the frequency range
                indices = np.where((frequency_axis >= freq_min) & (frequency_axis <= freq_max))

                # Adjust the magnitude in the frequency domain
                modified_spectrum[indices] *= amplification_factor
            
            frequency_ranges = [(-2500,-200),(-20000,-2500),(0,0) , (0,0)] #lion, elephant cat dog           
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
            self.input.data_line = self.plotWidget4.plot(
                self.input.time_axis, modified_signal, name=self.input.name
            )
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
                self.unifromSlider1, self.unifromSlider2, self.unifromSlider3, self.unifromSlider4,
                self.unifromSlider5, self.unifromSlider6, self.unifromSlider7, self.unifromSlider8,
                self.unifromSlider9, self.unifromSlider10
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
            self.input.data_line = self.plotWidget4.plot(
                self.input.time_axis, modified_signal, name=self.input.name
            )
            self.generate_spectrogram(self.input.time_axis,modified_signal,self.input.fs,2)
            # self.plotWidget4.setXRange(0, self.input.time_axis.max())
            self.plotWidget3.setLabel('left', 'Amplitude')
            self.plotWidget3.setLabel('bottom', 'Frequency (Hz)')
        
    def plotFrequencyDomain(self,frequency_axis,modified_spectrum,positive_freq_indices):
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

        # Get the slider values
        medical_sliders = [
            self.medicalSignalSlider1, self.medicalSignalSlider1, self.medicalSignalSlider1, self.medicalSignalSlider1
        ]

        # Calculate the arythmia frequencies
        arythmia_freq = set(self.input.FrequencySamples) - set(self.input.uniform_fftfreq)
        
        # Find the indices of arythmia frequencies in the frequency array
        arythmia_indices = np.where(np.isin(self.input.FrequencySamples, list(arythmia_freq)))

        for slider in medical_sliders:
            amplification_factor = slider.value() / 10.0  # Normalize the slider value to [0, 1]
            amplitude = amplification_factor * 2  # Square the amplitude for increased effect
            modified_spectrum[arythmia_indices] *= amplitude

        self.plotFrequencyDomain(self.input.FrequencySamples, modified_spectrum,positive_freq_indices)
        # Compute the inverse Fourier Transform to get the modified signal
        modified_signal = np.fft.ifft(modified_spectrum).real

        # Print the lengths for debugging
        print(len(modified_signal))
        print(len(self.input.time_axis))

        # Update the plot with the modified signal in the time domain
        # self.plotWidget4.clear()
        # self.input.data_line = self.plotWidget4.plot(
        #     self.input.time_axis, modified_signal, name=self.input.name
        # )
