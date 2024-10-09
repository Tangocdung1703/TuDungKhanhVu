print("Ứng dụng tạo bộ lọc âm thanh")

# import sympy as sym
# import numpy as np
# import matplotlib.pyplot as plt
# from sympy.discrete.transforms import fft
# from sympy.discrete.transforms import ifft
# Fs = 100                       # sampling rate
# Ts = 1.0/Fs                      # sampling interval
# t = np.arange(0,1,Ts)            # time vector
# ff = 5                           # frequency of the signal
# #y = np.random.randn(Fs)
# y = np.sin(2 * np.pi * ff * t)
# plt.subplot(3,1,1)
# plt.plot(t,y,'k-')
# plt.xlabel('time')
# plt.ylabel('amplitude')

# plt.subplot(3,1,2)
# Y = fft(y)# fft computing and normalization
# y1 = []
# for i in Y:
#     i = complex(i)
#     y1.append(abs(i.real))
# print(y1)
# n1 = len(y1)//2
# plt.plot(range(n1),y1[0:n1], 'r-')
# plt.xlabel('freq (Hz)')
# plt.ylabel('|Y(freq)|')
# plt.show()

import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sympy.discrete.transforms import fft, ifft
import threading
import queue

# --- Hàm xử lý ---
def generate_signal():
    global Fs, Ts, t, ff, y
    Fs = int(entry_Fs.get())  # Lấy giá trị Fs từ input
    Ts = 1.0/Fs              
    t = np.arange(0,1,Ts)
    ff = int(entry_ff.get())  # Lấy giá trị ff từ input
    y = np.sin(2 * np.pi * ff * t)
    # Gửi tín hiệu đến luồng xử lý vẽ đồ thị
    signal_queue.put(y)

def plot_signal():
    global fig, ax1, ax2

    while True:
        try:
            # Lấy tín hiệu từ hàng đợi
            y = signal_queue.get(block=False)

            # Xóa đồ thị cũ nếu có
            for widget in frame_plot.winfo_children():
                widget.destroy()

            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 5))

            # Vẽ tín hiệu thời gian
            ax1.plot(t, y, 'k-')
            ax1.set_xlabel('Thời gian (s)')
            ax1.set_ylabel('Biên độ')
            ax1.set_title('Tín hiệu âm thanh')

            # Tính toán và vẽ phổ tần số
            Y = fft(y)
            n = len(Y) // 2
            freq = np.fft.fftfreq(y.size, d=Ts)[:n]
            Y_abs = np.abs(Y[:n]) / n
            ax2.plot(freq, Y_abs, 'r-')
            ax2.set_xlabel('Tần số (Hz)')
            ax2.set_ylabel('|Y(f)|')
            ax2.set_title('Phổ tần số')

            # Hiển thị đồ thị trong frame_plot
            canvas = FigureCanvasTkAgg(fig, master=frame_plot)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        except queue.Empty:
            # Không có tín hiệu nào trong hàng đợi, tiếp tục chờ
            pass

        # Lên lịch cho hàm này chạy lại sau 100ms
        window.after(100, process_signal)


def apply_filter():
    global y_filtered
    
    filter_type = filter_var.get()
    cutoff_freq = int(entry_cutoff.get())
    
    # Tính toán phổ tần số
    Y = fft(y)
    n = len(Y) // 2
    freq = np.fft.fftfreq(y.size, d=Ts)[:n]
    
    # Áp dụng bộ lọc
    if filter_type == 'lowpass':
        H = (np.abs(freq) <= cutoff_freq).astype(float)
    elif filter_type == 'highpass':
        H = (np.abs(freq) > cutoff_freq).astype(float)
    elif filter_type == 'bandpass':
        f1 = int(entry_f1.get())
        f2 = int(entry_f2.get())
        H = ((np.abs(freq) >= f1) & (np.abs(freq) <= f2)).astype(float)
    else:
        H = np.ones(n)
    
    # Áp dụng bộ lọc lên phổ tần số
    Y_filtered = Y[:n] * H
    
    # Chuyển đổi ngược về miền thời gian
    y_filtered = np.fft.irfft(np.concatenate((Y_filtered, np.flip(Y_filtered))))

    # Cập nhật đồ thị
    plot_filtered_signal()

def plot_filtered_signal():
    global fig, ax1, ax2
    
    # Xóa đồ thị cũ
    ax1.clear()
    ax2.clear()
    
    # Vẽ tín hiệu thời gian sau khi lọc
    ax1.plot(t, y_filtered, 'b-')
    ax1.set_xlabel('Thời gian (s)')
    ax1.set_ylabel('Biên độ')
    ax1.set_title('Tín hiệu sau khi lọc')

    # Tính toán và vẽ phổ tần số sau khi lọc
    Y_filtered_full = fft(y_filtered)
    n = len(Y_filtered_full) // 2
    freq = np.fft.fftfreq(y_filtered.size, d=Ts)[:n]
    Y_filtered_abs = np.abs(Y_filtered_full[:n]) / n
    ax2.plot(freq, Y_filtered_abs, 'g-')
    ax2.set_xlabel('Tần số (Hz)')
    ax2.set_ylabel('|Y(f)|')
    ax2.set_title('Phổ tần số sau khi lọc')

    # Cập nhật đồ thị
    fig.canvas.draw_idle()


# --- Giao diện đồ họa ---
window = tk.Tk()
window.title("Ứng dụng tạo bộ lọc âm thanh")
# Tạo hàng đợi để lưu trữ tín hiệu
signal_queue = queue.Queue()
# --- Frame chứa input ---
frame_input = tk.Frame(window)
frame_input.pack(pady=10)

# --- Nhập Fs ---
label_Fs = tk.Label(frame_input, text="Tần số lấy mẫu (Fs):")
label_Fs.grid(row=0, column=0)
entry_Fs = tk.Entry(frame_input)
entry_Fs.grid(row=0, column=1)
entry_Fs.insert(0, "100")  # Giá trị mặc định

# --- Nhập ff ---
label_ff = tk.Label(frame_input, text="Tần số tín hiệu (ff):")
label_ff.grid(row=1, column=0)
entry_ff = tk.Entry(frame_input)
entry_ff.grid(row=1, column=1)
entry_ff.insert(0, "5")  # Giá trị mặc định

# --- Nút tạo tín hiệu ---
button_generate = tk.Button(frame_input, text="Tạo tín hiệu", command=generate_signal)
button_generate.grid(row=0, column=2, rowspan=2)

# --- Frame chứa bộ lọc ---
frame_filter = tk.Frame(window)
frame_filter.pack(pady=10)

# --- Chọn loại bộ lọc ---
filter_label = tk.Label(frame_filter, text="Chọn bộ lọc:")
filter_label.grid(row=0, column=0)
filter_var = tk.StringVar(value="lowpass")
filter_options = ["lowpass", "highpass", "bandpass"]
filter_dropdown = ttk.Combobox(frame_filter, textvariable=filter_var, values=filter_options)
filter_dropdown.grid(row=0, column=1)

# --- Nhập tần số cắt ---
label_cutoff = tk.Label(frame_filter, text="Tần số cắt:")
label_cutoff.grid(row=1, column=0)
entry_cutoff = tk.Entry(frame_filter)
entry_cutoff.grid(row=1, column=1)

# --- Nhập f1 và f2 cho bandpass ---
label_f1 = tk.Label(frame_filter, text="F1:")
label_f1.grid(row=2, column=0)
entry_f1 = tk.Entry(frame_filter)
entry_f1.grid(row=2, column=1)

label_f2 = tk.Label(frame_filter, text="F2:")
label_f2.grid(row=3, column=0)
entry_f2 = tk.Entry(frame_filter)
entry_f2.grid(row=3, column=1)

# --- Nút áp dụng bộ lọc ---
button_apply = tk.Button(frame_filter, text="Áp dụng", command=apply_filter)
button_apply.grid(row=1, column=2, rowspan=3)

# --- Frame chứa đồ thị ---
frame_plot = tk.Frame(window)
frame_plot.pack(fill=tk.BOTH, expand=True)

# Tạo và chạy luồng xử lý tín hiệu
signal_thread = threading.Thread(target=plot_signal)
signal_thread.daemon = True  # Cho phép luồng kết thúc khi luồng chính kết thúc
signal_thread.start()

window.mainloop()
