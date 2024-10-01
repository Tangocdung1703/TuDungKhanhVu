import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# --- Signal Parameters ---
samplingFrequency = 100  # Hz
samplingInterval = 1 / samplingFrequency  # s
beginTime = 0  # s
endTime = 10  # s
signal1Frequency = 4  # Hz
signal2Frequency = 7  # Hz

# --- Time Domain Setup ---
time = np.arange(beginTime, endTime, samplingInterval)
amplitude1 = np.sin(2 * np.pi * signal1Frequency * time)
amplitude2 = np.sin(2 * np.pi * signal2Frequency * time)
amplitude = amplitude1 + amplitude2

# --- Frequency Domain Calculation ---
fourierTransform = np.fft.fft(amplitude) / len(amplitude)
fourierTransform = fourierTransform[range(int(len(amplitude) / 2))]
tpCount = len(amplitude)
values = np.arange(int(tpCount / 2))
timePeriod = tpCount / samplingFrequency
frequencies = values / timePeriod

# --- GUI Setup ---
fig, ax = plt.subplots(4, 1)
plt.subplots_adjust(hspace=1, bottom=0.3)  # Adjust spacing for widgets

# --- Plots ---
timePlot1, = ax[0].plot(time, amplitude1, label='Signal 1')
timePlot2, = ax[1].plot(time, amplitude2, label='Signal 2')
timePlotCombined, = ax[2].plot(time, amplitude, label='Combined')
freqPlot, = ax[3].plot(frequencies, abs(fourierTransform), label='Frequency Spectrum')

# --- Labels ---
ax[0].set_title('Sine wave with a frequency of 4 Hz')
ax[0].set_xlabel('Time (s)')
ax[0].set_ylabel('Amplitude')
ax[1].set_title('Sine wave with a frequency of 7 Hz')
ax[1].set_xlabel('Time (s)')
ax[1].set_ylabel('Amplitude')
ax[2].set_title('Combined Signal')
ax[2].set_xlabel('Time (s)')
ax[2].set_ylabel('Amplitude')
ax[3].set_title('Fourier Transform')
ax[3].set_xlabel('Frequency (Hz)')
ax[3].set_ylabel('Magnitude')

# --- Filter Slider ---
axFreq = plt.axes([0.25, 0.15, 0.65, 0.03])  # Position of the slider
cutoffFreq = Slider(axFreq, 'Cutoff Frequency (Hz)', 0.1, 10, valinit=4)


# --- Filter Function ---
def filter_signal(val):
    cutoff = cutoffFreq.val
    filtered_transform = np.where(frequencies <= cutoff, fourierTransform, 0)  # Apply filter in frequency domain
    filtered_signal = np.fft.irfft(filtered_transform * len(amplitude))  # Inverse FFT to get time domain
    timePlotCombined.set_ydata(filtered_signal)  # Update combined signal plot
    freqPlot.set_ydata(np.abs(filtered_transform))  # Update frequency plot
    fig.canvas.draw_idle()


cutoffFreq.on_changed(filter_signal)

# --- Reset Button ---
resetAx = plt.axes([0.8, 0.025, 0.1, 0.04])
resetButton = Button(resetAx, 'Reset', hovercolor='0.975')


def reset(event):
    cutoffFreq.reset()  # Reset slider to default
    timePlotCombined.set_ydata(amplitude)  # Reset to original combined signal
    freqPlot.set_ydata(abs(fourierTransform))
    fig.canvas.draw_idle()


resetButton.on_clicked(reset)

plt.show()