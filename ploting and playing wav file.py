import wave
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from PyQt5 import QtWidgets, QtCore
import threading

class WaveformPlotter(QtWidgets.QWidget):
    def __init__(self, signal, frame_rate):
        super().__init__()

        self.signal = signal
        self.frame_rate = frame_rate
        self.index = 0

        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [])
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Amplitude')
        self.ax.set_title('Waveform of your_file.wav')

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.fig.canvas)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(20)  # Adjust the interval for smoother updates
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

        self.sound_stream = sd.OutputStream(channels=1, samplerate=self.frame_rate, callback=self.callback)
        self.sound_stream.start()

        self.show()

    def update_plot(self):
        if self.index < len(self.signal):
            x_data = np.linspace(0, self.index / self.frame_rate, num=self.index + 1)
            y_data = self.signal[: self.index + 1]
            self.line.set_xdata(x_data)
            self.line.set_ydata(y_data)

            # Adjust the x-axis and y-axis limits based on the current data
            self.ax.set_xlim(0, x_data[-1] + 1)  # Set the x-axis range dynamically
            self.ax.set_ylim(np.min(y_data), np.max(y_data) + 10)  # Set the y-axis range dynamically

            self.index += int(self.frame_rate * 0.02)  # Increment based on a small time interval for smoother updates
            self.fig.canvas.draw()

    def callback(self, outdata, frames, time, status):
        if self.index < len(self.signal):
            y_data = self.signal[self.index : self.index + frames]
            outdata[:len(y_data), 0] = y_data
            if len(y_data) < len(outdata):
                outdata[len(y_data):, 0] = 0  # Zero-padding
            self.index += frames
        else:
            outdata[:, 0] = 0  # Zero-padding if needed
            self.timer.stop()


def load():
    with wave.open('source_file.wav', 'rb') as wave_file:
        # Extract Raw Audio from Wav File
        signal = wave_file.readframes(-1)
        signal = np.frombuffer(signal, dtype='int16')

        # Get the frame rate
        frame_rate = wave_file.getframerate()

        app = QtWidgets.QApplication([])  # Create a PyQt application
        plotter = WaveformPlotter(signal, frame_rate)
        app.exec_()

if __name__ == '__main__':
    load()