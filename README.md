# Signal Equalizer App

## Introduction

Signal Equalizer is a versatile desktop application designed for use in the music and speech industry, as well as various biomedical applications such as hearing aid abnormalities detection. The application empowers users to open a signal, manipulate the magnitude of specific frequency components using sliders, and reconstruct the modified signal. Signal Equalizer operates in different modes to cater to diverse use cases.

## Features

### 1. Uniform Range Mode
In this mode, the total frequency range of the input signal is divided uniformly into 10 equal ranges of frequencies. Each range is controlled by a dedicated slider in the user interface (UI). This mode facilitates a comprehensive understanding of the impact on each frequency when an equalizer action is taken.

### 2. Musical Instruments Mode
Users can switch to this mode to control the magnitude of specific musical instruments in the input music signal. The input music signal should be a mixture of at least four different musical instruments.

### 3. Animal Sounds Mode
In this mode, users can control the magnitude of specific animal sounds in a mixture of at least four animal sounds.

### 4. ECG Abnormalities Mode
Users can choose from four ECG signals - one normal and three with specific types of arrhythmias. Each slider in this mode controls the magnitude of the arrhythmia component in the input signal.

### 5. Multiplication/Smoothing Windows
Users can apply four multiplication/smoothing windows (Rectangle, Hamming, Hanning, Gaussian) to the frequency range multiplied by the corresponding slider value. The UI allows users to choose the smoothing window, customize its parameters visually, and apply it to the equalizer.

### 6. Mode Switching
Users can easily switch between modes, with the UI adapting dynamically. The main changes in UI when switching modes include variations in slider captions and potentially the number of sliders.

### 7. Signal Viewers
The UI features two linked cine signal viewers—one for the input and one for the output signals. These viewers include a full set of functionality panel (play/stop/pause/speed-control/zoom/pan/reset). The viewers are precisely linked, ensuring they show the same time-part of the signal synchronously.

### 8. Spectrograms
Two spectrograms, one for the input and one for the output signals, provide visual representations of the signal's frequency content. The output spectrogram reflects changes made using the equalizer sliders. Users can toggle the visibility of the spectrograms.

## Validation
To validate the application, users should prepare a synthetic signal file, composed of a summation of several pure single frequencies across the entire frequency range. This synthetic signal helps track the impact of equalizer actions on each frequency.

## Getting Started

1. Clone the repository.
2. Install dependencies.
3. Run the application.

## Contributors

- Shehap Elhadary
- Abdurahman Hesham
- Mohamed Ibrahim

We appreciate the contributions of the above individuals to the development of the Signal Equalizer application. 
