import numpy as np

class PlotLine:
    def __init__(self):
        self.time_axis = None
        self.sound_axis = None
        self.index = 0
        self.data_line = None
        self.pen = None
        self.name = None
        self.fs=None
        self.fft = None
        self.FrequencySamples = None
        self.uniform_fftfreq=None
        self.uniform_fft=None

    def SetData(self,data, fs):
        n = len(data)  # the length of the arrays contained in data
        # Working with stereo audio, there are two channels in the audio data.
        # Let's retrieve each channel seperately:
        ch1 = np.array([data[i][0] for i in range(n)])  # channel 1

        # x-axis and y-axis to plot the audio data
        self.time_axis = np.linspace(0, n / fs, n, endpoint=False)
        self.sound_axis = ch1
        self.fft = np.fft.fft(self.sound_axis)
        self.FrequencySamples = np.fft.fftfreq(len(self.sound_axis), 1/fs)
