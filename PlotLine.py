import numpy as np

class PlotLine:
    def __init__(self):
        self.time_axis = None
        self.sound_axis = None
        self.index = 0
        self.data_line = None
        self.pen = None
        self.name = None

    def SetData(self,data, fs):
        n = len(data)  # the length of the arrays contained in data
        # Working with stereo audio, there are two channels in the audio data.
        # Let's retrieve each channel seperately:
        ch1 = np.array([data[i][0] for i in range(n)])  # channel 1
        ch2 = np.array([data[i][1] for i in range(n)])  # channel 2

        # x-axis and y-axis to plot the audio data
        self.time_axis = np.linspace(0, n / fs, n, endpoint=False)
        self.sound_axis = ch1
