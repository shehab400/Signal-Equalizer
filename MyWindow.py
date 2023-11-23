from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import QThread,QObject,pyqtSignal as Signal, pyqtSlot as Slot
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
from PyQt5.QtWidgets import QApplication,QMainWindow,QVBoxLayout,QPushButton,QWidget,QErrorMessage,QMessageBox,QDialog,QScrollBar,QSlider
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
import numpy as np
import math
import audio2numpy as a2n
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import pygame
import os

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
        self.ui.verticalSlider_11.valueChanged.connect(self.KeyboardAdjustor)

        pygame.mixer.init()
        self.worker = Worker()
        self.worker_thread = QThread()

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
        #
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
        if self.ui.stackedWidget.currentIndex() == 1:
            self.ComposedLoad()

    def ComposedLoad(self):
        if self.ui.stackedWidget.currentIndex() == 1:
            self.sounds = []
            for i in range(4):
                filename = QtWidgets.QFileDialog.getOpenFileName()
                path = filename[0]
                self.sounds.append(AudioSegment.from_mp3(path))
                
            self.UpdateComposed()

            pygame.mixer.music.load("ComposedSound.mp3")
            pygame.mixer.music.play()

            self.plotWidget1.setXRange(0,10,padding=0)
            self.plotWidget1.setMouseEnabled(x=False,y=False)

            self.work_requested.emit(math.ceil(self.newplot.time_axis.max()))

    def UpdateComposed(self):
        #self.SoundMerge(self.sounds[0],self.sounds[1],self.sounds[2],self.sounds[3])
        data, fs = a2n.audio_from_file("ComposedSound.mp3")
        
        self.newplot = PlotLine()
        self.newplot.name = "ComposedSound"
        self.newplot.fs=fs
        self.newplot.SetData(data,fs)
        self.plotWidget1.clear()
        self.newplot.data_line = self.plotWidget1.plot(self.newplot.time_axis,self.newplot.sound_axis,name=self.newplot.name)

    def SoundMerge(self,sound0,sound1,sound2,sound3):
        self.composed = sound0.overlay(sound1,position=0)
        self.composed = self.composed.overlay(sound2,position=0)
        self.composed = self.composed.overlay(sound3,position=0)
        self.composed.export("ComposedSound.mp3",format="mp3")

    def KeyboardAdjustor(self):
        if self.sounds != None:
            NewSound = self.sounds[0] + ((self.musicSlider1.value()-5)*2)
            pos = pygame.mixer.music.get_pos()
            pygame.mixer.music.unload()
            if os.path.exists('ComposedSound.mp3'):
                os.remove("ComposedSound.mp3")
            self.SoundMerge(NewSound,self.sounds[1],self.sounds[2],self.sounds[3])
            self.UpdateComposed()
            pygame.mixer.music.load("ComposedSound.mp3")
            pygame.mixer.music.play()
            #pygame.mixer.music.set_pos(pos)

    def random_color(self):
        red = random.randint(0,255)
        green = random.randint(0,255)
        blue = random.randint(0,255)
        
        return (red,green,blue)
    

    def UpdatePlots(self):
        # random_rgb = self.random_color()
        # self.newplot.pen = pg.mkPen(color = random_rgb)
        # self.newplot.data_line.setPen(self.newplot.pen)
        self.plotWidget1.setXRange(pygame.mixer.music.get_pos()/1000, (pygame.mixer.music.get_pos()/1000)+10, padding=0)

    def Complete(self):
        self.plotWidget1.setXRange(0,self.newplot.time_axis.max())
        
    def generate_spectrogram(self, time_axis, sound_axis, fs):
    # Calculate the spectrogram using numpy and scipy
        f, t, Sxx = np.histogram2d(
            sound_axis,
            time_axis,
            bins=(128, 128),  # Reduce the number of bins
            range=[[sound_axis.min(), sound_axis.max()], [time_axis.min(), time_axis.max()]]
        )

        # Create a PlotItem for the spectrogram
        img = pg.ImageItem()
        img.setImage(Sxx.T, autoLevels=True)
        img.scale((time_axis.max() - time_axis.min()) / Sxx.shape[0], (sound_axis.max() - sound_axis.min()) / Sxx.shape[1])

        # Set axis labels
        img.getView().setLabels(bottom='Time (s)', left='Frequency (Hz)')

        # Add the spectrogram to the PlotWidget
        self.plotWidget2.addItem(img)

    def update_frequency_components(self):
        # Compute the Fourier Transform for the original signal
        original_spectrum = np.fft.fft(self.newplot.sound_axis)

        # Calculate the frequency resolution and create the frequency axis
        time_step = 1.0 / self.newplot.fs
        frequency_axis = np.fft.fftfreq(len(self.newplot.sound_axis), time_step)

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

        # Initialize an array for the modified spectrum
        modified_spectrum = np.copy(original_spectrum)

        # Adjust the magnitudes based on the slider values, with increased amplification
        for slider, (freq_min, freq_max) in zip(uniform_sliders, frequency_ranges):
            amplification_factor = slider.value() / 10.0  # Normalize the slider value to [0, 1]
            amplitude = amplification_factor * 2  # Square the amplitude for increased effect

            # Find the indices of the frequency range
            indices = np.where((frequency_axis >= freq_min) & (frequency_axis <= freq_max))

            # Adjust the magnitude in the frequency domain
            modified_spectrum[indices] *= amplitude

        # Update the plot with the original signal and the modified signal in the frequency domain
        self.plotWidget2.clear()
        self.plotWidget2.plot(
            frequency_axis[positive_freq_indices],
            np.abs(original_spectrum[positive_freq_indices]),
            pen='b',
            name='Original Spectrum'
        )
        self.plotWidget2.setLabel('left', 'Amplitude')
        self.plotWidget2.setLabel('bottom', 'Frequency (Hz)')

        self.plotWidget3.clear()
        self.plotWidget3.plot(
            frequency_axis[positive_freq_indices],
            np.abs(modified_spectrum[positive_freq_indices]),
            pen='r',
            name='Modified Spectrum'
        )
        self.plotWidget3.setLabel('left', 'Amplitude')
        self.plotWidget3.setLabel('bottom', 'Frequency (Hz)')

        # Compute the inverse Fourier Transform to get the modified signal
        modified_signal = np.fft.ifft(modified_spectrum).real

        # Update the plot with the modified signal in the time domain
        self.plotWidget4.clear()
        self.newplot.data_line = self.plotWidget4.plot(
            self.newplot.time_axis, modified_signal, name=self.newplot.name
        )
        self.plotWidget4.setXRange(0, self.newplot.time_axis.max())
        self.plotWidget4.setMouseEnabled(x=False, y=False)
