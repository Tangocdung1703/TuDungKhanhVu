import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog

# Define a function to read CSV file
def read_csv_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        df = pd.read_csv(file_path, index_col=0, header=0)
        global in_data, df_filtered, in_data_filtered
        in_data = df.to_numpy()
        df_filtered = df[df.index.isin(range(1, 10))]
        in_data_filtered = df_filtered.to_numpy()
        show_all_data()

# Functions to display data
def show_all_data():
    text_area.delete('1.0', tk.END)
    text_area.insert(tk.END, df_filtered.to_string())

def show_total_students():
    tongsv = in_data_filtered[:, 1]
    total_students = np.sum(tongsv)
    text_area.delete('1.0', tk.END)
    text_area.insert(tk.END, f"Tổng số sinh viên đi thi: {total_students}\n\n")
    for i, sv in enumerate(tongsv, start=1):
        text_area.insert(tk.END, f"Lớp {i}: {sv} sinh viên\n")

def show_max_scores():
    diemA_plus = in_data_filtered[:, 2]
    diemA = in_data_filtered[:, 3]
    diemB_plus = in_data_filtered[:, 4]
    diemB = in_data_filtered[:, 5]
    diemC_plus = in_data_filtered[:, 6]
    diemC = in_data_filtered[:, 7]
    diemD_plus = in_data_filtered[:, 8]
    diemD = in_data_filtered[:, 9]
    diemF = in_data_filtered[:, 10]
    max_a_plus = df_filtered.index[np.argmax(diemA_plus)]
    max_a = df_filtered.index[np.argmax(diemA)]
    max_b_plus = df_filtered.index[np.argmax(diemB_plus)]
    max_b = df_filtered.index[np.argmax(diemB)]
    max_c_plus = df_filtered.index[np.argmax(diemC_plus)]
    max_c = df_filtered.index[np.argmax(diemC)]
    max_d_plus = df_filtered.index[np.argmax(diemD_plus)]
    max_d = df_filtered.index[np.argmax(diemD)]
    max_f = df_filtered.index[np.argmax(diemF)]
    text_area.delete('1.0', tk.END)
    text_area.insert(tk.END, f"Lớp có nhiều điểm A+ nhất: {max_a_plus}\n")
    text_area.insert(tk.END, f"Lớp có nhiều điểm A nhất: {max_a}\n")
    text_area.insert(tk.END, f"Lớp có nhiều điểm B+ nhất: {max_b_plus}\n")
    text_area.insert(tk.END, f"Lớp có nhiều điểm B nhất: {max_b}\n")
    text_area.insert(tk.END, f"Lớp có nhiều điểm C+ nhất: {max_c_plus}\n")
    text_area.insert(tk.END, f"Lớp có nhiều điểm C nhất: {max_c}\n")
    text_area.insert(tk.END, f"Lớp có nhiều điểm D+ nhất: {max_d_plus}\n")
    text_area.insert(tk.END, f"Lớp có nhiều điểm D nhất: {max_d}\n")
    text_area.insert(tk.END, f"Lớp có nhiều điểm F nhất: {max_f}\n")

def show_statistics():
    plt.figure()
    diemA_plus = in_data_filtered[:, 2]
    diemA = in_data_filtered[:, 3]
    diemB_plus = in_data_filtered[:, 4]
    diemB = in_data_filtered[:, 5]
    diemC_plus = in_data_filtered[:, 6]
    diemC = in_data_filtered[:, 7]
    diemD_plus = in_data_filtered[:, 8]
    diemD = in_data_filtered[:, 9]
    diemF = in_data_filtered[:, 10]
    plt.plot(range(len(diemA_plus)), diemA_plus, 'm-', label="Điểm A+")
    plt.plot(range(len(diemA)), diemA, 'r-', label="Điểm A")
    plt.plot(range(len(diemB_plus)), diemB_plus, 'g-', label="Điểm B+")
    plt.plot(range(len(diemB)), diemB, 'b-', label="Điểm B")
    plt.plot(range(len(diemC_plus)), diemC_plus, 'c-', label="Điểm C+")
    plt.plot(range(len(diemC)), diemC, 'y-', label="Điểm C")
    plt.plot(range(len(diemD_plus)), diemD_plus, 'orange', label="Điểm D+")
    plt.plot(range(len(diemD)), diemD, 'k-', label="Điểm D")
    plt.plot(range(len(diemF)), diemF, 'purple', label="Điểm F")
    plt.xlabel("Lớp")
    plt.ylabel("Số sinh viên đạt điểm")
    plt.legend(loc='upper right')
    plt.title("Thống kê điểm")
    plt.show()


def show_output_standard():
    plt.figure()
    l1 = in_data_filtered[:, 11]
    l2 = in_data_filtered[:, 12]
    plt.plot(range(len(l1)), l1, 'r-', label="L1")
    plt.plot(range(len(l2)), l2, 'g-', label="L2")
    plt.xlabel("Lớp")
    plt.ylabel("Chuẩn đầu ra")
    plt.legend(loc='upper right')
    plt.title("Chuẩn đầu ra")
    plt.show()


def show_regular_scores():
    plt.figure()
    tx1 = in_data_filtered[:, 13]
    tx2 = in_data_filtered[:, 14]
    plt.plot(range(len(tx1)), tx1, 'r-', label="TX1")
    plt.plot(range(len(tx2)), tx2, 'g-', label="TX2")
    plt.xlabel("Lớp")
    plt.ylabel("Điểm thường xuyên")
    plt.legend(loc='upper right')
    plt.title("Điểm thường xuyên")
    plt.show()


def show_final_scores():
    plt.figure()
    final_scores = in_data_filtered[:, 15]
    plt.plot(range(len(final_scores)), final_scores, 'b-', label="Điểm cuối kỳ")
    plt.xlabel("Lớp")
    plt.ylabel("Điểm cuối kỳ")
    plt.legend(loc='upper right')
    plt.title("Điểm cuối kỳ")
    plt.show()


# Tạo cửa sổ chính
root = tk.Tk()
root.title("Quản lý điểm")
root.geometry("1500x500")  # Đặt kích thước cửa sổ lớn hơn

# Tạo khung cho các nút
frame_buttons = ttk.Frame(root)
frame_buttons.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

# Tạo khung cho khu vực hiển thị văn bản
frame_text = ttk.Frame(root)
frame_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Tạo các nút lựa chọn
btn_load_data = ttk.Button(frame_buttons, text="Nhập dữ liệu từ file CSV", command=read_csv_file)
btn_all_data = ttk.Button(frame_buttons, text="Hiển thị toàn bộ dữ liệu", command=show_all_data)
btn_total_students = ttk.Button(frame_buttons, text="Tổng số sinh viên đi thi", command=show_total_students)
btn_max_scores = ttk.Button(frame_buttons, text="Lớp có nhiều điểm nhất", command=show_max_scores)
btn_statistics = ttk.Button(frame_buttons, text="Thống kê điểm", command=show_statistics)
btn_output_standard = ttk.Button(frame_buttons, text="Chuẩn đầu ra", command=show_output_standard)
btn_regular_scores = ttk.Button(frame_buttons, text="Điểm thường xuyên", command=show_regular_scores)
btn_final_scores = ttk.Button(frame_buttons, text="Điểm cuối kỳ", command=show_final_scores)

# Đặt các nút lên khung
btn_load_data.pack(pady=5)
btn_all_data.pack(pady=5)
btn_total_students.pack(pady=5)
btn_max_scores.pack(pady=5)
btn_statistics.pack(pady=5)
btn_output_standard.pack(pady=5)
btn_regular_scores.pack(pady=5)
btn_final_scores.pack(pady=5)

# Tạo khu vực hiển thị văn bản
text_area = scrolledtext.ScrolledText(frame_text, width=100, height=80)  # Đặt kích thước khu vực văn bản lớn hơn
text_area.pack(fill=tk.BOTH, expand=True)

# Chạy ứng dụng
root.mainloop()