import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, welch
import wave
import pygame
import pandas as pd
import pywt

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav"), ("CSV Files", "*.csv"), ("Text Files", "*.txt")])
    if file_path.endswith('.wav'):
        print(f"Tệp đã chọn: {file_path}")
        with wave.open(file_path, 'rb') as wf:
            n_samples = wf.getnframes()
            global signal
            signal = np.frombuffer(wf.readframes(n_samples), dtype=np.int16)
        plot_signal(signal)
    elif file_path.endswith('.csv'):
        print(f"Tệp đã chọn: {file_path}")
        df = pd.read_csv(file_path)
        signal = df.iloc[:, 0].values
        plot_signal(signal)
    elif file_path.endswith('.txt'):
        print(f"Tệp đã chọn: {file_path}")
        signal = np.loadtxt(file_path)
        plot_signal(signal)
    else:
        messagebox.showerror("Lỗi", "Không thể tải tín hiệu. Vui lòng chọn tệp WAV, CSV hoặc TXT hợp lệ.")

def filter_signal(signal, filter_type):
    if signal.size == 0:
        messagebox.showerror("Lỗi", "Chưa có tín hiệu để lọc.")
        return
    if filter_type == "lowpass":
        b, a = butter(5, 0.2)
    elif filter_type == "highpass":
        b, a = butter(5, 0.2, btype='high')
    elif filter_type == "bandpass":
        b, a = butter(5, [0.1, 0.3], btype='band')
    elif filter_type == "bandstop":
        b, a = butter(5, [0.1, 0.3], btype='stop')
    filtered_signal = lfilter(b, a, signal)
    plt.figure()
    plt.plot(filtered_signal)
    plt.title(f"Tín hiệu sau khi lọc {filter_type}")
    plt.show()

def plot_signal(signal):
    if signal.size == 0:
        messagebox.showerror("Lỗi", "Chưa có tín hiệu để hiển thị.")
        return
    plt.figure()
    plt.plot(signal)
    plt.title("Đồ thị tín hiệu")
    plt.show()

def apply_fft(signal):
    if signal.size == 0:
        messagebox.showerror("Lỗi", "Chưa có tín hiệu để phân tích.")
        return
    fft_signal = np.fft.fft(signal)
    freq = np.fft.fftfreq(len(signal))
    plt.figure()
    plt.plot(freq, np.abs(fft_signal))
    plt.title("Phổ Fourier của tín hiệu")
    plt.show()

def apply_wavelet(signal):
    if signal.size == 0:
        messagebox.showerror("Lỗi", "Chưa có tín hiệu để phân tích.")
        return
    coeffs = pywt.wavedec(signal, 'db1')
    plt.figure()
    for i, coeff in enumerate(coeffs):
        plt.subplot(len(coeffs), 1, i + 1)
        plt.plot(coeff)
        plt.title(f"Wavelet Coefficients Level {i}")
    plt.show()

def main():
    global signal
    signal = np.array([])  # Khởi tạo tín hiệu
    root = tk.Tk()
    root.title("Xử lý tín hiệu số")

    label = tk.Label(root, text="Chào mừng bạn đến với ứng dụng Xử lý tín hiệu số")
    label.pack()

    button_load = tk.Button(root, text="Tải tín hiệu(CSV, WAV, TEXT)", command=load_file)
    button_load.pack()

    # Thêm các ô nhập liệu cho các thông số tín hiệu
    tk.Label(root, text="Tần số:").pack()
    entry_freq = tk.Entry(root)
    entry_freq.pack()

    tk.Label(root, text="Biên độ:").pack()
    entry_amplitude = tk.Entry(root)
    entry_amplitude.pack()

    button_generate = tk.Button(root, text="Tạo tín hiệu", command=lambda: generate_signal(entry_freq.get(), entry_amplitude.get()))
    button_generate.pack()

    button_lowpass = tk.Button(root, text="Lọc thông thấp", command=lambda: filter_signal(signal, "lowpass"))
    button_highpass = tk.Button(root, text="Lọc thông cao", command=lambda: filter_signal(signal, "highpass"))
    button_bandpass = tk.Button(root, text="Lọc thông dải", command=lambda: filter_signal(signal, "bandpass"))
    button_bandstop = tk.Button(root, text="Lọc chặn dải", command=lambda: filter_signal(signal, "bandstop"))
    button_lowpass.pack()
    button_highpass.pack()
    button_bandpass.pack()
    button_bandstop.pack()

    button_plot = tk.Button(root, text="Hiển thị đồ thị", command=lambda: plot_signal(signal))
    button_plot.pack()

    button_fft = tk.Button(root, text="Phân tích Fourier", command=lambda: apply_fft(signal))
    button_fft.pack()

    button_wavelet = tk.Button(root, text="Phân tích Wavelet", command=lambda: apply_wavelet(signal))
    button_wavelet.pack()

    root.mainloop()

def generate_signal(freq, amplitude):
    if not freq or not amplitude:
        messagebox.showerror("Lỗi", "Phải nhập thông số tần số và biên độ trước khi tạo tín hiệu.")
        return
    t = np.linspace(0, 1, 500)
    freq = float(freq)
    amplitude = float(amplitude)
    global signal
    signal = amplitude * np.sin(2 * np.pi * freq * t)
    print("Tín hiệu đã được tạo thành công!")
    plot_signal(signal)

if __name__ == "__main__":
    main()
