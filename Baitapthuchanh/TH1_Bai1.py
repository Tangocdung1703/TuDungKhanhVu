import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import numpy as np

def giai_he_pt_gauss(he_so):
    try:
        A = np.array(he_so, dtype=float)
        n = len(A)

        # Chuyển về ma trận bậc thang
        for i in range(n):
            # Tìm phần tử chéo khác 0
            if A[i, i] == 0:
                for k in range(i + 1, n):
                    if A[k, i] != 0:
                        A[[i, k]] = A[[k, i]]
                        break
                else:
                    # Kiểm tra xem có phải vô số nghiệm hay không
                    # Nếu tất cả phần tử ở cột i từ dòng i+1 đều bằng 0 
                    # và phần tử cuối cùng của dòng i khác 0 thì vô nghiệm
                    if all(A[j, i] == 0 for j in range(i + 1, n)) and A[i, -1] != 0:
                        return "Vô nghiệm"
                    else:
                        return "Vô số nghiệm"

            # Loại bỏ các phần tử cùng cột với phần tử chéo
            for j in range(i + 1, n):
                factor = A[j, i] / A[i, i]
                A[j, :] -= factor * A[i, :]

        # Tìm nghiệm
        nghiem = np.zeros(n)
        for i in range(n - 1, -1, -1):
            nghiem[i] = (A[i, -1] - np.sum(A[i, i+1:n] * nghiem[i+1:n])) / A[i, i]

        return nghiem
    except:
        return "Lỗi"

# Hàm xử lý giải hệ phương trình (có thể thêm các phương pháp khác)
def giai_he_pt():
    try:
        n = int(entry_so_an.get())
        he_so = []
        for i in range(n):
            hang = []
            for j in range(n + 1):
                gia_tri = entry_he_so[i][j].get()
                if gia_tri == "":
                    messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ hệ số!")
                    return
                hang.append(float(gia_tri))
            he_so.append(hang)

        # Gọi hàm giải hệ phương trình
        nghiem = giai_he_pt_gauss(he_so)

        if isinstance(nghiem, str):  # Kiểm tra xem kết quả là string (lỗi, vô nghiệm, vô số nghiệm)
            label_ket_qua.config(text=nghiem) 
        elif nghiem is None:
            label_ket_qua.config(text="Đã xảy ra lỗi")
        else:
            ket_qua = "Nghiệm của hệ phương trình là:\n"
            for i in range(n):
                ket_qua += f"x{i + 1} = {nghiem[i]:.2f}\n"
            label_ket_qua.config(text=ket_qua)
    except:
        messagebox.showerror("Lỗi", "Đã xảy ra lỗi. Vui lòng kiểm tra lại dữ liệu!")

# Hàm tạo bảng nhập hệ số
def tao_bang_nhap_he_so(n):
    global entry_he_so
    entry_he_so = []
    for i in range(n):
        hang = []
        for j in range(n + 1):
            entry = tk.Entry(frame_nhap_lieu, width=5)
            entry.grid(row=i + 1, column=j + 1)
            hang.append(entry)
        entry_he_so.append(hang)

# Hàm xử lý sự kiện khi thay đổi số ẩn
def thay_doi_so_an(event=None):
    try:
        n = int(entry_so_an.get())
        if n > 0:
            for widget in frame_nhap_lieu.winfo_children():
                widget.destroy()

            # Tạo lại label cho các biến
            for i in range(n):
                label = tk.Label(frame_nhap_lieu, text=f"X{i + 1}")
                label.grid(row=0, column=i + 1)

            # Tạo lại label cho vế phải
            label = tk.Label(frame_nhap_lieu, text="=Y")
            label.grid(row=0, column=n + 1)

            tao_bang_nhap_he_so(n)
    except:
        messagebox.showerror("Lỗi", "Số ẩn phải là số nguyên dương!")

# # Tạo cửa sổ chính
# window = tk.Tk()
# window.title("Giải Hệ Phương Trình Tuyến Tính")
# window.geometry("500x350")  # Thiết lập kích thước
# # Tạo frame cho số ẩn
# frame_so_an = tk.Frame(window)
# frame_so_an.pack(pady=10)

# label_so_an = tk.Label(frame_so_an, text="Số ẩn:")
# label_so_an.pack(side=tk.LEFT)

# entry_so_an = tk.Entry(frame_so_an, width=5)
# entry_so_an.pack(side=tk.LEFT)
# entry_so_an.insert(0, "3") # Mặc định là hệ 3 ẩn
# entry_so_an.bind("<Return>", thay_doi_so_an)

# button_thay_doi = tk.Button(frame_so_an, text="Thay đổi", command=thay_doi_so_an)
# button_thay_doi.pack(side=tk.LEFT)

# # Tạo frame cho bảng nhập liệu
# frame_nhap_lieu = tk.Frame(window)
# frame_nhap_lieu.pack()

# # Tạo bảng nhập hệ số ban đầu (3 ẩn)
# thay_doi_so_an()

# # Tạo nút giải hệ phương trình
# button_giai = tk.Button(window, text="Giải hệ phương trình", command=giai_he_pt)
# button_giai.pack(pady=10)

# # Tạo frame hiển thị kết quả
# frame_ket_qua = tk.Frame(window)
# frame_ket_qua.pack()

# label_ket_qua = tk.Label(frame_ket_qua, text="")
# label_ket_qua.pack()

# window.mainloop()

# Tạo cửa sổ chính
window = tk.Tk()
window.title("Giải Hệ Phương Trình Tuyến Tính")
window.geometry("500x350")
import os
icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
window.iconbitmap(icon_path) # Thêm biểu tượng cho cửa sổ

# Tạo style cho các widget
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=10)
style.configure("TEntry", font=("Arial", 12), padding=5)

# Tạo frame cho số ẩn
frame_so_an = ttk.Frame(window)
frame_so_an.pack(pady=10)

label_so_an = ttk.Label(frame_so_an, text="Số ẩn:", font=("Arial", 12))
label_so_an.pack(side=tk.LEFT)

entry_so_an = ttk.Entry(frame_so_an, width=5, font=("Arial", 12))
entry_so_an.pack(side=tk.LEFT)
entry_so_an.insert(0, "3") # Mặc định là hệ 3 ẩn
entry_so_an.bind("<Return>", thay_doi_so_an)

button_thay_doi = ttk.Button(frame_so_an, text="Thay đổi", command=thay_doi_so_an)
button_thay_doi.pack(side=tk.LEFT)

# Tạo frame cho bảng nhập liệu
frame_nhap_lieu = ttk.Frame(window)
frame_nhap_lieu.pack(pady=10)

# Tạo bảng nhập hệ số ban đầu (3 ẩn)
thay_doi_so_an()

# Tạo nút giải hệ phương trình
button_giai = ttk.Button(window, text="Giải hệ phương trình", command=giai_he_pt, style="TButton")
button_giai.pack(pady=10)

# Tạo frame hiển thị kết quả
frame_ket_qua = ttk.Frame(window)
frame_ket_qua.pack()

label_ket_qua = ttk.Label(frame_ket_qua, text="", font=("Arial", 12))
label_ket_qua.pack()

window.mainloop()