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
#
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


# Hàm tạo tín hiệu
def tao_tin_hieu(f, A, loai, t):
    if loai == "sin":
        return A * np.sin(2 * np.pi * f * t)
    elif loai == "cos":
        return A * np.cos(2 * np.pi * f * t)
    elif loai == "vuong":
        return A * np.sign(np.sin(2 * np.pi * f * t))
    elif loai == "rang_cua":
        return A * (2 * f * t - np.floor(2 * f * t))
    else:
        return np.zeros_like(t)


# Hàm tính FFT
def tinh_fft(y):
    Y = fft(y)
    y1 = [abs(complex(i).real) for i in Y]
    n1 = len(y1) // 2
    return range(n1), y1[0:n1]


def loc_tin_hieu(y, loai_loc, f_cut):
    Y = fft(y)
    n = len(y)
    freq = np.fft.fftfreq(n, d=Ts)
    if loai_loc == "low-pass":
        indices = np.where(np.abs(freq) > f_cut)[0]
        Y[indices] = 0
    elif loai_loc == "high-pass":
        indices = np.where(np.abs(freq) < f_cut)[0]
        Y[indices] = 0
    elif loai_loc == "band-pass":
        indices_low = np.where(np.abs(freq) < f_cut[0])[0]
        indices_high = np.where(np.abs(freq) > f_cut[1])[0]
        Y[indices_low] = 0
        Y[indices_high] = 0
    elif loai_loc == "band-stop":
        indices_low = np.where(np.abs(freq) < f_cut[0])[0]
        indices_high = np.where(np.abs(freq) > f_cut[1])[0]
        Y[indices_low] = 0
        Y[indices_high] = 0
    return ifft(Y)


# Hàm ghép tín hiệu
def ghep_tin_hieu(f_list, A_list, loai_list, t):
    y = np.zeros_like(t)
    for f, A, loai in zip(f_list, A_list, loai_list):
        y += tao_tin_hieu(f, A, loai, t)
    return y


# Hàm lưu tín hiệu
def luu_tin_hieu(y, filename):
    np.savetxt(filename + ".txt", y)


# Hàm cập nhật đồ thị
def cap_nhat_do_thi(y, t, title=""):
    global fig, canvas
    fig.clf()
    ax = fig.add_subplot(111)
    ax.plot(t, y, 'k-')
    ax.set_xlabel('Thời gian')
    ax.set_ylabel('Biên độ')
    ax.set_title(title)
    canvas.draw()


# Hàm xử lý chức năng tạo tín hiệu
def tao_tin_hieu_click():
    global y, t
    f = float(entry_f.get())
    A = float(entry_A.get())
    loai = combo_loai.get()
    y = tao_tin_hieu(f, A, loai, t)
    cap_nhat_do_thi(y, t, title="Tín hiệu gốc")


# Hàm xử lý chức năng phổ tần
def tinh_phu_tan_click():
    global y, t
    freq, Y = tinh_fft(y)
    cap_nhat_do_thi(Y, freq, title="Phổ tần")


def loc_tin_hieu_click():
    global y, t
    loai_loc = combo_loai_loc.get()
    if loai_loc == "band-pass" or loai_loc == "band-stop":
        try:
            f_cut1 = float(entry_f_cut1.get())
            f_cut2 = float(entry_f_cut2.get())
            if f_cut1 <= 0 or f_cut2 <= 0 or f_cut1 >= f_cut2:
                tk.messagebox.showerror("Lỗi", "Tần số cắt không hợp lệ.")
                return
            f_cut = [f_cut1, f_cut2]
        except ValueError:
            tk.messagebox.showerror("Lỗi", "Vui lòng nhập tần số cắt hợp lệ.")
            return
    else:
        try:
            f_cut = float(entry_f_cut.get())
            if f_cut <= 0:
                tk.messagebox.showerror("Lỗi", "Tần số cắt không hợp lệ.")
                return
        except ValueError:
            tk.messagebox.showerror("Lỗi", "Vui lòng nhập tần số cắt hợp lệ.")
            return
    y = loc_tin_hieu(y, loai_loc, f_cut)
    cap_nhat_do_thi(y, t, title="Tín hiệu đã lọc")


# Hàm xử lý chức năng ghép tín hiệu
def ghep_tin_hieu_click():
    global y, t
    f_list = []
    A_list = []
    loai_list = []
    num_signals = int(entry_num_signals.get())
    for i in range(num_signals):
        f_list.append(float(entry_f_list[i].get()))
        A_list.append(float(entry_A_list[i].get()))
        loai_list.append(combo_loai_list[i].get())
    y = ghep_tin_hieu(f_list, A_list, loai_list, t)
    cap_nhat_do_thi(y, t, title="Tín hiệu ghép")


# Hàm xử lý chức năng lưu tín hiệu
def luu_tin_hieu_click():
    filename = entry_filename.get()
    luu_tin_hieu(y, filename)


# Khởi tạo thông số
Fs = 100
Ts = 1.0 / Fs
t = np.arange(0, 1, Ts)
y = np.zeros_like(t)

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Ứng dụng xử lý tín hiệu số")

# Tạo khung cho hướng dẫn sử dụng
frame_guide = tk.Frame(root)
frame_guide.pack(fill=tk.X)

# Tạo label cho hướng dẫn
label_guide = tk.Label(frame_guide, text="Hướng dẫn sử dụng:", font=("Arial", 12, "bold"))
label_guide.pack(pady=10)

# Tạo label cho hướng dẫn chi tiết
label_guide_detail = tk.Label(frame_guide, text="""
    1. Tạo tín hiệu: Nhập thông tin tần số, biên độ và loại tín hiệu.
    2. Phổ tần: Hiển thị đồ thị phổ tần của tín hiệu.
    3. Lọc tín hiệu: Chọn loại bộ lọc và nhập tần số cắt.
    4. Ghép tín hiệu: Nhập số lượng tín hiệu và thông tin của mỗi tín hiệu.
    5. Lưu tín hiệu: Nhập tên file để lưu tín hiệu.
    """, justify=tk.LEFT)
label_guide_detail.pack(pady=10)

# Tạo khung cho đồ thị
frame_graph = tk.Frame(root)
frame_graph.pack(fill=tk.BOTH, expand=True)

# Tạo figure và canvas cho đồ thị
fig = plt.Figure(figsize=(5, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=frame_graph)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Tạo khung cho các chức năng
frame_functions = tk.Frame(root)
frame_functions.pack(fill=tk.X)

# Tạo phần tạo tín hiệu
frame_tao_tin_hieu = tk.Frame(frame_functions)
frame_tao_tin_hieu.pack(side=tk.LEFT, padx=10)

# Tạo label và entry cho tần số
label_f = tk.Label(frame_tao_tin_hieu, text="Tần số (Hz):")
label_f.pack()
entry_f = tk.Entry(frame_tao_tin_hieu)
entry_f.pack()

# Tạo label và entry cho biên độ
label_A = tk.Label(frame_tao_tin_hieu, text="Biên độ:")
label_A.pack()
entry_A = tk.Entry(frame_tao_tin_hieu)
entry_A.pack()

# Tạo combobox cho loại tín hiệu
label_loai = tk.Label(frame_tao_tin_hieu, text="Loại tín hiệu:")
label_loai.pack()
combo_loai = ttk.Combobox(frame_tao_tin_hieu, values=["sin", "cos", "vuong", "rang_cua"])
combo_loai.current(0)
combo_loai.pack()

# Tạo button tạo tín hiệu
button_tao_tin_hieu = tk.Button(frame_tao_tin_hieu, text="Tạo tín hiệu", command=tao_tin_hieu_click)
button_tao_tin_hieu.pack(pady=10)

# Tạo phần phổ tần
frame_phu_tan = tk.Frame(frame_functions)
frame_phu_tan.pack(side=tk.LEFT, padx=10)

# Tạo button tính FFT
button_phu_tan = tk.Button(frame_phu_tan, text="Phổ tần", command=tinh_phu_tan_click)
button_phu_tan.pack()

# Tạo phần lọc tín hiệu
frame_loc_tin_hieu = tk.Frame(frame_functions)
frame_loc_tin_hieu.pack(side=tk.LEFT, padx=10)

# Tạo combobox cho loại bộ lọc
label_loai_loc = tk.Label(frame_loc_tin_hieu, text="Loại bộ lọc:")
label_loai_loc.pack()
combo_loai_loc = ttk.Combobox(frame_loc_tin_hieu, values=["low-pass", "high-pass", "band-pass", "band-stop"])
combo_loai_loc.current(0)
combo_loai_loc.pack()

# Tạo label và entry cho tần số cắt
label_f_cut = tk.Label(frame_loc_tin_hieu, text="Tần số cắt (Hz):")
label_f_cut.pack()
entry_f_cut = tk.Entry(frame_loc_tin_hieu)
entry_f_cut.pack()

# Tạo label và entry cho tần số cắt thấp
label_f_cut1 = tk.Label(frame_loc_tin_hieu, text="Tần số cắt thấp (Hz):")
label_f_cut1.pack()
entry_f_cut1 = tk.Entry(frame_loc_tin_hieu)
entry_f_cut1.pack()

# Tạo label và entry cho tần số cắt cao
label_f_cut2 = tk.Label(frame_loc_tin_hieu, text="Tần số cắt cao (Hz):")
label_f_cut2.pack()
entry_f_cut2 = tk.Entry(frame_loc_tin_hieu)
entry_f_cut2.pack()

# Tạo button lọc tín hiệu
button_loc_tin_hieu = tk.Button(frame_loc_tin_hieu, text="Lọc tín hiệu", command=loc_tin_hieu_click)
button_loc_tin_hieu.pack(pady=10)

# Tạo phần ghép tín hiệu
frame_ghep_tin_hieu = tk.Frame(frame_functions)
frame_ghep_tin_hieu.pack(side=tk.LEFT, padx=10)

# Tạo label và entry cho số lượng tín hiệu
label_num_signals = tk.Label(frame_ghep_tin_hieu, text="Số lượng tín hiệu:")
label_num_signals.pack()
entry_num_signals = tk.Entry(frame_ghep_tin_hieu)
entry_num_signals.pack()

# Tạo list cho các entry của tần số, biên độ và loại tín hiệu
entry_f_list = []
entry_A_list = []
combo_loai_list = []


# Hàm tạo các phần tử động cho ghép tín hiệu
def tao_phan_tu_ghep(num_signals):
    global entry_f_list, entry_A_list, combo_loai_list
    for i in range(num_signals):
        # Tạo label và entry cho tần số
        label_f = tk.Label(frame_ghep_tin_hieu, text=f"Tần số {i + 1} (Hz):")
        label_f.pack()
        entry_f = tk.Entry(frame_ghep_tin_hieu)
        entry_f.pack()
        entry_f_list.append(entry_f)

        # Tạo label và entry cho biên độ
        label_A = tk.Label(frame_ghep_tin_hieu, text=f"Biên độ {i + 1}:")
        label_A.pack()
        entry_A = tk.Entry(frame_ghep_tin_hieu)
        entry_A.pack()
        entry_A_list.append(entry_A)

        # Tạo combobox cho loại tín hiệu
        label_loai = tk.Label(frame_ghep_tin_hieu, text=f"Loại {i + 1}:")
        label_loai.pack()
        combo_loai = ttk.Combobox(frame_ghep_tin_hieu, values=["sin", "cos", "vuong", "rang_cua"])
        combo_loai.current(0)
        combo_loai.pack()
        combo_loai_list.append(combo_loai)


# Hàm xử lý khi thay đổi số lượng tín hiệu ghép
def thay_doi_so_luong_ghep():
    global entry_f_list, entry_A_list, combo_loai_list
    num_signals = int(entry_num_signals.get())

    # Xóa các phần tử cũ
    for entry_f in entry_f_list:
        entry_f.destroy()
    for entry_A in entry_A_list:
        entry_A.destroy()
    for combo_loai in combo_loai_list:
        combo_loai.destroy()
    entry_f_list.clear()
    entry_A_list.clear()
    combo_loai_list.clear()

    # Tạo các phần tử mới
    tao_phan_tu_ghep(num_signals)


# Tạo button ghép tín hiệu
button_ghep_tin_hieu = tk.Button(frame_ghep_tin_hieu, text="Ghép tín hiệu", command=ghep_tin_hieu_click)
button_ghep_tin_hieu.pack(pady=10)

# Thêm button thay đổi số lượng tín hiệu
button_thay_doi_ghep = tk.Button(frame_ghep_tin_hieu, text="Thay đổi", command=thay_doi_so_luong_ghep)
button_thay_doi_ghep.pack(pady=5)

# Tạo phần lưu tín hiệu
frame_luu_tin_hieu = tk.Frame(frame_functions)
frame_luu_tin_hieu.pack(side=tk.LEFT, padx=10)

# Tạo label và entry cho tên file
label_filename = tk.Label(frame_luu_tin_hieu, text="Tên file:")
label_filename.pack()
entry_filename = tk.Entry(frame_luu_tin_hieu)
entry_filename.pack()

# Tạo button lưu tín hiệu
button_luu_tin_hieu = tk.Button(frame_luu_tin_hieu, text="Lưu tín hiệu", command=luu_tin_hieu_click)
button_luu_tin_hieu.pack(pady=10)

# Chạy ứng dụng
root.mainloop()