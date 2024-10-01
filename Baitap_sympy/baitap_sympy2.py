import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# -- Hàm xử lý cho các chức năng hình học --

def tinh_khoang_cach():
    try:
        x1 = float(entry_x1.get())
        y1 = float(entry_y1.get())
        x2 = float(entry_x2.get())
        y2 = float(entry_y2.get())
        khoang_cach = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        ket_qua_label.config(text=f"Khoảng cách: {khoang_cach:.2f}")
    except ValueError:
        ket_qua_label.config(text="Lỗi: Vui lòng nhập số.")

def ve_duong_thang():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())

        x = np.linspace(-10, 10, 200)
        y = a*x + b

        ax.clear()
        ax.plot(x, y)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title("Đồ thị đường thẳng y = ax + b")
        ax.grid(True)
        canvas.draw()
    except ValueError:
        ket_qua_label.config(text="Lỗi: Vui lòng nhập số.")

def tinh_dien_tich_tam_giac():
    try:
        x1 = float(entry_x1_tam_giac.get())
        y1 = float(entry_y1_tam_giac.get())
        x2 = float(entry_x2_tam_giac.get())
        y2 = float(entry_y2_tam_giac.get())
        x3 = float(entry_x3_tam_giac.get())
        y3 = float(entry_y3_tam_giac.get())
        dien_tich = 1/2 * abs((x2*y3 - x3*y2) - (x1*y3 - x3*y1) + (x1*y2 - x2*y1))
        ket_qua_label.config(text=f"Diện tích tam giác: {dien_tich:.2f}")
    except ValueError:
        ket_qua_label.config(text="Lỗi: Vui lòng nhập số.")

def tim_trung_diem():
    try:
        x1 = float(entry_x1.get())
        y1 = float(entry_y1.get())
        x2 = float(entry_x2.get())
        y2 = float(entry_y2.get())
        trung_diem_x = (x1 + x2) / 2
        trung_diem_y = (y1 + y2) / 2
        ket_qua_label.config(text=f"Trung điểm: ({trung_diem_x:.2f}, {trung_diem_y:.2f})")
    except ValueError:
        ket_qua_label.config(text="Lỗi: Vui lòng nhập số.")

def kiem_tra_tam_giac():
    try:
        a = float(entry_canh_a.get())
        b = float(entry_canh_b.get())
        c = float(entry_canh_c.get())

        if a + b > c and a + c > b and b + c > a:
            if a == b == c:
                loai_tam_giac = "Tam giác đều"
            elif a == b or a == c or b == c:
                loai_tam_giac = "Tam giác cân"
            elif a**2 + b**2 == c**2 or a**2 + c**2 == b**2 or b**2 + c**2 == a**2:
                loai_tam_giac = "Tam giác vuông"
            else:
                loai_tam_giac = "Tam giác thường"
            ket_qua_label.config(text=f"Loại tam giác: {loai_tam_giac}")
        else:
            ket_qua_label.config(text="Ba cạnh không tạo thành tam giác.")
    except ValueError:
        ket_qua_label.config(text="Lỗi: Vui lòng nhập số.")

# -- Giao diện đồ họa --

window = tk.Tk()
window.title("Ứng dụng Hỗ trợ Hình học")

# Tạo Notebook (tab)
notebook = ttk.Notebook(window)
notebook.pack(expand=True, fill="both")

# --- Tab Khoảng cách ---
tab_khoang_cach = ttk.Frame(notebook)
notebook.add(tab_khoang_cach, text="Khoảng cách")

label_diem1 = ttk.Label(tab_khoang_cach, text="Điểm 1 (x1, y1):")
label_diem1.grid(row=0, column=0, padx=5, pady=5)
entry_x1 = ttk.Entry(tab_khoang_cach)
entry_x1.grid(row=0, column=1, padx=5, pady=5)
entry_y1 = ttk.Entry(tab_khoang_cach)
entry_y1.grid(row=0, column=2, padx=5, pady=5)

label_diem2 = ttk.Label(tab_khoang_cach, text="Điểm 2 (x2, y2):")
label_diem2.grid(row=1, column=0, padx=5, pady=5)
entry_x2 = ttk.Entry(tab_khoang_cach)
entry_x2.grid(row=1, column=1, padx=5, pady=5)
entry_y2 = ttk.Entry(tab_khoang_cach)
entry_y2.grid(row=1, column=2, padx=5, pady=5)

button_tinh_khoang_cach = ttk.Button(tab_khoang_cach, text="Tính khoảng cách", command=tinh_khoang_cach)
button_tinh_khoang_cach.grid(row=2, column=0, columnspan=3, pady=10)

# --- Tab Đường thẳng ---
tab_duong_thang = ttk.Frame(notebook)
notebook.add(tab_duong_thang, text="Đường thẳng")

label_a = ttk.Label(tab_duong_thang, text="Nhập a:")
label_a.grid(row=0, column=0, padx=5, pady=5)
entry_a = ttk.Entry(tab_duong_thang)
entry_a.grid(row=0, column=1, padx=5, pady=5)

label_b = ttk.Label(tab_duong_thang, text="Nhập b:")
label_b.grid(row=1, column=0, padx=5, pady=5)
entry_b = ttk.Entry(tab_duong_thang)
entry_b.grid(row=1, column=1, padx=5, pady=5)

button_ve_duong_thang = ttk.Button(tab_duong_thang, text="Vẽ đường thẳng", command=ve_duong_thang)
button_ve_duong_thang.grid(row=2, column=0, columnspan=2, pady=10)

# --- Tab Tam giác ---
tab_tam_giac = ttk.Frame(notebook)
notebook.add(tab_tam_giac, text="Tam giác")

label_diem1_tam_giac = ttk.Label(tab_tam_giac, text="Điểm 1 (x1, y1):")
label_diem1_tam_giac.grid(row=0, column=0, padx=5, pady=5)
entry_x1_tam_giac = ttk.Entry(tab_tam_giac)
entry_x1_tam_giac.grid(row=0, column=1, padx=5, pady=5)
entry_y1_tam_giac = ttk.Entry(tab_tam_giac)
entry_y1_tam_giac.grid(row=0, column=2, padx=5, pady=5)

label_diem2_tam_giac = ttk.Label(tab_tam_giac, text="Điểm 2 (x2, y2):")
label_diem2_tam_giac.grid(row=1, column=0, padx=5, pady=5)
entry_x2_tam_giac = ttk.Entry(tab_tam_giac)
entry_x2_tam_giac.grid(row=1, column=1, padx=5, pady=5)
entry_y2_tam_giac = ttk.Entry(tab_tam_giac)
entry_y2_tam_giac.grid(row=1, column=2, padx=5, pady=5)

label_diem3_tam_giac = ttk.Label(tab_tam_giac, text="Điểm 3 (x3, y3):")
label_diem3_tam_giac.grid(row=2, column=0, padx=5, pady=5)
entry_x3_tam_giac = ttk.Entry(tab_tam_giac)
entry_x3_tam_giac.grid(row=2, column=1, padx=5, pady=5)
entry_y3_tam_giac = ttk.Entry(tab_tam_giac)
entry_y3_tam_giac.grid(row=2, column=2, padx=5, pady=5)

button_tinh_dien_tich_tam_giac = ttk.Button(tab_tam_giac, text="Tính diện tích", command=tinh_dien_tich_tam_giac)
button_tinh_dien_tich_tam_giac.grid(row=3, column=0, columnspan=3, pady=10)

# --- Tab Trung điểm ---
tab_trung_diem = ttk.Frame(notebook)
notebook.add(tab_trung_diem, text="Trung điểm")

label_diem1_trung_diem = ttk.Label(tab_trung_diem, text="Điểm 1 (x1, y1):")
label_diem1_trung_diem.grid(row=0, column=0, padx=5, pady=5)
entry_x1_trung_diem = ttk.Entry(tab_trung_diem)
entry_x1_trung_diem.grid(row=0, column=1, padx=5, pady=5)
entry_y1_trung_diem = ttk.Entry(tab_trung_diem)
entry_y1_trung_diem.grid(row=0, column=2, padx=5, pady=5)

label_diem2_trung_diem = ttk.Label(tab_trung_diem, text="Điểm 2 (x2, y2):")
label_diem2_trung_diem.grid(row=1, column=0, padx=5, pady=5)
entry_x2_trung_diem = ttk.Entry(tab_trung_diem)
entry_x2_trung_diem.grid(row=1, column=1, padx=5, pady=5)
entry_y2_trung_diem = ttk.Entry(tab_trung_diem)
entry_y2_trung_diem.grid(row=1, column=2, padx=5, pady=5)

button_tim_trung_diem = ttk.Button(tab_trung_diem, text="Tìm trung điểm", command=tim_trung_diem)
button_tim_trung_diem.grid(row=2, column=0, columnspan=3, pady=10)

# --- Tab Kiểm tra tam giác ---
tab_kiem_tra_tam_giac = ttk.Frame(notebook)
notebook.add(tab_kiem_tra_tam_giac, text="Kiểm tra tam giác")

label_canh_a = ttk.Label(tab_kiem_tra_tam_giac, text="Nhập cạnh a:")
label_canh_a.grid(row=0, column=0, padx=5, pady=5)
entry_canh_a = ttk.Entry(tab_kiem_tra_tam_giac)
entry_canh_a.grid(row=0, column=1, padx=5, pady=5)

label_canh_b = ttk.Label(tab_kiem_tra_tam_giac, text="Nhập cạnh b:")
label_canh_b.grid(row=1, column=0, padx=5, pady=5)
entry_canh_b = ttk.Entry(tab_kiem_tra_tam_giac)
entry_canh_b.grid(row=1, column=1, padx=5, pady=5)

label_canh_c = ttk.Label(tab_kiem_tra_tam_giac, text="Nhập cạnh c:")
label_canh_c.grid(row=2, column=0, padx=5, pady=5)
entry_canh_c = ttk.Entry(tab_kiem_tra_tam_giac)
entry_canh_c.grid(row=2, column=1, padx=5, pady=5)

button_kiem_tra_tam_giac = ttk.Button(tab_kiem_tra_tam_giac, text="Kiểm tra tam giác", command=kiem_tra_tam_giac)
button_kiem_tra_tam_giac.grid(row=3, column=0, columnspan=2, pady=10)

# --- Khung hiển thị kết quả ---
ket_qua_label = ttk.Label(window, text="", wraplength=300)
ket_qua_label.pack(pady=10)

# --- Khung vẽ đồ thị ---
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

window.mainloop()
