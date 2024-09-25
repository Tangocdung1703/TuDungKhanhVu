import numpy as np
import tkinter as tk
from tkinter import messagebox

# Hàm giải hệ phương trình tuyến tính
def giai_he_pt(A, B):
  try:
    A_inv = np.linalg.inv(A)
    X = np.dot(A_inv, B)
    return X
  except np.linalg.LinAlgError:
    return None

# Hàm cộng hai ma trận
def cong_ma_tran(A, B):
  try:
    return np.add(A, B)
  except ValueError:
    return None

# Hàm trừ hai ma trận
def tru_ma_tran(A, B):
  try:
    return np.subtract(A, B)
  except ValueError:
    return None

# Hàm nhân hai ma trận
def nhan_ma_tran(A, B):
  try:
    return np.dot(A, B)
  except ValueError:
    return None

# Hàm chia hai ma trận
def chia_ma_tran(A, B):
  try:
    return np.divide(A, B)
  except ValueError:
    return None

# Hàm tìm ma trận nghịch đảo
def tim_ma_tran_nghich_dao(A):
  try:
    return np.linalg.inv(A)
  except np.linalg.LinAlgError:
    return None

# Hàm tính hạng ma trận
def tinh_hang_ma_tran(A):
  return np.linalg.matrix_rank(A)

# Hàm xử lý khi nhấn nút "Giải"
def solve_system():
  try:
    n = int(entry_n.get())  # số phương trình và số ẩn
    A = np.zeros((n, n))  # ma trận hệ số
    B = np.zeros(n)  # ma trận hằng số

    # Lấy dữ liệu từ các ô nhập
    for i in range(n):
      for j in range(n):
        A[i, j] = float(entries_A[i][j].get())
      B[i] = float(entries_B[i].get())

    # Giải hệ phương trình
    result = giai_he_pt(A, B)
    if result is None:
      messagebox.showerror("Lỗi", "Hệ phương trình không có nghiệm hoặc vô số nghiệm")
    else:
      result_str = ', '.join([f"x{i + 1} = {result[i]:.2f}" for i in range(n)])
      messagebox.showinfo("Kết quả", f"Nghiệm của hệ là: {result_str}")
  except ValueError:
    messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ")

# Hàm xử lý khi nhấn nút "Cộng"
def cong_ma_tran_handle():
  try:
    m1 = int(entry_m1.get())  # số hàng ma trận 1
    n1 = int(entry_n1.get())  # số cột ma trận 1
    m2 = int(entry_m2.get())  # số hàng ma trận 2
    n2 = int(entry_n2.get())  # số cột ma trận 2
    if (m1 != m2) or (n1 != n2):
      messagebox.showerror("Lỗi", "Hai ma trận phải có cùng kích thước để cộng")
      return

    A = np.zeros((m1, n1))  # ma trận 1
    B = np.zeros((m2, n2))  # ma trận 2

    # Lấy dữ liệu từ các ô nhập
    for i in range(m1):
      for j in range(n1):
        A[i, j] = float(entries_A1[i][j].get())
    for i in range(m2):
      for j in range(n2):
        B[i, j] = float(entries_A2[i][j].get())

    # Thực hiện phép cộng
    result = cong_ma_tran(A, B)
    if result is None:
      messagebox.showerror("Lỗi", "Lỗi khi cộng hai ma trận")
    else:
      result_str = '\n'.join([' '.join([f"{x:.2f}" for x in row]) for row in result])
      messagebox.showinfo("Kết quả", f"Ma trận kết quả:\n{result_str}")
  except ValueError:
    messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ")

# Hàm xử lý khi nhấn nút "Trừ"
def tru_ma_tran_handle():
  try:
    m1 = int(entry_m1.get())  # số hàng ma trận 1
    n1 = int(entry_n1.get())  # số cột ma trận 1
    m2 = int(entry_m2.get())  # số hàng ma trận 2
    n2 = int(entry_n2.get())  # số cột ma trận 2
    if (m1 != m2) or (n1 != n2):
      messagebox.showerror("Lỗi", "Hai ma trận phải có cùng kích thước để trừ")
      return

    A = np.zeros((m1, n1))  # ma trận 1
    B = np.zeros((m2, n2))  # ma trận 2

    # Lấy dữ liệu từ các ô nhập
    for i in range(m1):
      for j in range(n1):
        A[i, j] = float(entries_A1[i][j].get())
    for i in range(m2):
      for j in range(n2):
        B[i, j] = float(entries_A2[i][j].get())

    # Thực hiện phép trừ
    result = tru_ma_tran(A, B)
    if result is None:
      messagebox.showerror("Lỗi", "Lỗi khi trừ hai ma trận")
    else:
      result_str = '\n'.join([' '.join([f"{x:.2f}" for x in row]) for row in result])
      messagebox.showinfo("Kết quả", f"Ma trận kết quả:\n{result_str}")
  except ValueError:
    messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ")

# Hàm xử lý khi nhấn nút "Nhân"
def nhan_ma_tran_handle():
  try:
    m1 = int(entry_m1.get())  # số hàng ma trận 1
    n1 = int(entry_n1.get())  # số cột ma trận 1
    m2 = int(entry_m2.get())  # số hàng ma trận 2
    n2 = int(entry_n2.get())  # số cột ma trận 2
    if n1 != m2:
      messagebox.showerror("Lỗi", "Số cột của ma trận 1 phải bằng số hàng của ma trận 2 để nhân")
      return

    A = np.zeros((m1, n1))  # ma trận 1
    B = np.zeros((m2, n2))  # ma trận 2

    # Lấy dữ liệu từ các ô nhập
    for i in range(m1):
      for j in range(n1):
        A[i, j] = float(entries_A1[i][j].get())
    for i in range(m2):
      for j in range(n2):
        B[i, j] = float(entries_A2[i][j].get())

    # Thực hiện phép nhân
    result = nhan_ma_tran(A, B)
    if result is None:
      messagebox.showerror("Lỗi", "Lỗi khi nhân hai ma trận")
    else:
      result_str = '\n'.join([' '.join([f"{x:.2f}" for x in row]) for row in result])
      messagebox.showinfo("Kết quả", f"Ma trận kết quả:\n{result_str}")
  except ValueError:
    messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ")

# Hàm xử lý khi nhấn nút "Chia"
def chia_ma_tran_handle():
  try:
    m1 = int(entry_m1.get())  # số hàng ma trận 1
    n1 = int(entry_n1.get())  # số cột ma trận 1
    m2 = int(entry_m2.get())  # số hàng ma trận 2
    n2 = int(entry_n2.get())  # số cột ma trận 2
    if (m1 != m2) or (n1 != n2):
      messagebox.showerror("Lỗi", "Hai ma trận phải có cùng kích thước để chia")
      return

    A = np.zeros((m1, n1))  # ma trận 1
    B = np.zeros((m2, n2))  # ma trận 2

    # Lấy dữ liệu từ các ô nhập
    for i in range(m1):
      for j in range(n1):
        A[i, j] = float(entries_A1[i][j].get())
    for i in range(m2):
      for j in range(n2):
        B[i, j] = float(entries_A2[i][j].get())

    # Thực hiện phép chia
    result = chia_ma_tran(A, B)
    if result is None:
      messagebox.showerror("Lỗi", "Lỗi khi chia hai ma trận")
    else:
      result_str = '\n'.join([' '.join([f"{x:.2f}" for x in row]) for row in result])
      messagebox.showinfo("Kết quả", f"Ma trận kết quả:\n{result_str}")
  except ValueError:
    messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ")

# Hàm xử lý khi nhấn nút "Nghịch đảo"
def tim_ma_tran_nghich_dao_handle():
  try:
    n = int(entry_n.get())  # số hàng và cột ma trận
    A = np.zeros((n, n))  # ma trận 

    # Lấy dữ liệu từ các ô nhập
    for i in range(n):
      for j in range(n):
        A[i, j] = float(entries_A[i][j].get())

    # Thực hiện tìm ma trận nghịch đảo
    result = tim_ma_tran_nghich_dao(A)
    if result is None:
      messagebox.showerror("Lỗi", "Ma trận không khả nghịch")
    else:
      result_str = '\n'.join([' '.join([f"{x:.2f}" for x in row]) for row in result])
      messagebox.showinfo("Kết quả", f"Ma trận nghịch đảo:\n{result_str}")
  except ValueError:
    messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ")

# Hàm xử lý khi nhấn nút "Hạng"
def tinh_hang_ma_tran_handle(entry_m=None):
  try:
    m = int(entry_m.get())  # số hàng ma trận
    n = int(entry_n.get())  # số cột ma trận
    A = np.zeros((m, n))  # ma trận 

    # Lấy dữ liệu từ các ô nhập
    for i in range(m):
      for j in range(n):
        A[i, j] = float(entries_A[i][j].get())

    # Thực hiện tính hạng ma trận
    result = tinh_hang_ma_tran(A)
    messagebox.showinfo("Kết quả", f"Hạng của ma trận là: {result}")
  except ValueError:
    messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ")

# Hàm để tạo các ô nhập cho ma trận hệ số và hằng số
def create_input_fields():
  try:
    n = int(entry_n.get())  # số phương trình và số ẩn
    for widget in frame_inputs.winfo_children():
      widget.destroy()  # Xóa các ô nhập trước đó

    global entries_A, entries_B
    entries_A = []
    entries_B = []

    # Tạo ô nhập cho ma trận hệ số A
    for i in range(n):
      row_entries = []
      for j in range(n):
        entry = tk.Entry(frame_inputs, width=5)
        entry.grid(row=i, column=j, padx=5, pady=5)
        row_entries.append(entry)
      entries_A.append(row_entries)

    # Tạo ô nhập cho ma trận hằng số B
    for i in range(n):
      entry = tk.Entry(frame_inputs, width=5)
      entry.grid(row=i, column=n, padx=5, pady=5)
      entries_B.append(entry)

  except ValueError:
    messagebox.showerror("Lỗi", "Vui lòng nhập số phương trình hợp lệ")

# Hàm để tạo các ô nhập cho ma trận 1 và 2
def create_input_fields_matrix():
  try:
    m1 = int(entry_m1.get())  # số hàng ma trận 1
    n1 = int(entry_n1.get())  # số cột ma trận 1
    m2 = int(entry_m2.get())  # số hàng ma trận 2
    n2 = int(entry_n2.get())  # số cột ma trận 2

    for widget in frame_inputs_matrix1.winfo_children():
      widget.destroy()
    for widget in frame_inputs_matrix2.winfo_children():
      widget.destroy()

    global entries_A1, entries_A2
    entries_A1 = []
    entries_A2 = []

    # Tạo ô nhập cho ma trận 1
    for i in range(m1):
      row_entries = []
      for j in range(n1):
        entry = tk.Entry(frame_inputs_matrix1, width=5)
        entry.grid(row=i, column=j, padx=5, pady=5)
        row_entries.append(entry)
      entries_A1.append(row_entries)

    # Tạo ô nhập cho ma trận 2
    for i in range(m2):
      row_entries = []
      for j in range(n2):
        entry = tk.Entry(frame_inputs_matrix2, width=5)
        entry.grid(row=i, column=j, padx=5, pady=5)
        row_entries.append(entry)
      entries_A2.append(row_entries)

  except ValueError:
    messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ")

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Giải hệ phương trình tuyến tính và xử lý ma trận")

# Frame cho nhập số phương trình và số ẩn
frame_top = tk.Frame(root)
frame_top.pack(padx=10, pady=10)

label_n = tk.Label(frame_top, text="Số phương trình và số ẩn:")
label_n.pack(side=tk.LEFT)

entry_n = tk.Entry(frame_top, width=5)
entry_n.pack(side=tk.LEFT, padx=5)

btn_create_fields = tk.Button(frame_top, text="Tạo", command=create_input_fields)
btn_create_fields.pack(side=tk.LEFT, padx=5)

# Frame cho các ô nhập hệ số và hằng số
frame_inputs = tk.Frame(root)
frame_inputs.pack(padx=10, pady=10)

# Nút giải hệ phương trình
btn_solve = tk.Button(root, text="Giải", command=solve_system)
btn_solve.pack(padx=10, pady=10)

# Nút tìm ma trận nghịch đảo
btn_inverse = tk.Button(root, text="Nghịch đảo", command=tim_ma_tran_nghich_dao_handle)
btn_inverse.pack(padx=10, pady=10)

# Nút tính hạng ma trận
btn_rank = tk.Button(root, text="Hạng", command=tinh_hang_ma_tran_handle)
btn_rank.pack(padx=10, pady=10)

# --- Frame cho nhập số hàng và số cột của ma trận ---
frame_matrix_size = tk.Frame(root)
frame_matrix_size.pack(padx=10, pady=10)

label_m1 = tk.Label(frame_matrix_size, text="Số hàng ma trận 1:")
label_m1.pack(side=tk.LEFT)

entry_m1 = tk.Entry(frame_matrix_size, width=5)
entry_m1.pack(side=tk.LEFT, padx=5)

label_n1 = tk.Label(frame_matrix_size, text="Số cột ma trận 1:")
label_n1.pack(side=tk.LEFT)

entry_n1 = tk.Entry(frame_matrix_size, width=5)
entry_n1.pack(side=tk.LEFT, padx=5)

label_m2 = tk.Label(frame_matrix_size, text="Số hàng ma trận 2:")
label_m2.pack(side=tk.LEFT)

entry_m2 = tk.Entry(frame_matrix_size, width=5)
entry_m2.pack(side=tk.LEFT, padx=5)

label_n2 = tk.Label(frame_matrix_size, text="Số cột ma trận 2:")
label_n2.pack(side=tk.LEFT)

entry_n2 = tk.Entry(frame_matrix_size, width=5)
entry_n2.pack(side=tk.LEFT, padx=5)

btn_create_fields_matrix = tk.Button(frame_matrix_size, text="Tạo", command=create_input_fields_matrix)
btn_create_fields_matrix.pack(side=tk.LEFT, padx=5)

# --- Frame cho nhập ma trận 1 ---
frame_inputs_matrix1 = tk.Frame(root)
frame_inputs_matrix1.pack(padx=10, pady=10)

# --- Frame cho nhập ma trận 2 ---
frame_inputs_matrix2 = tk.Frame(root)
frame_inputs_matrix2.pack(padx=10, pady=10)

# Nút cộng hai ma trận
btn_cong = tk.Button(root, text="Cộng", command=cong_ma_tran_handle)
btn_cong.pack(padx=10, pady=10)

# Nút trừ hai ma trận
btn_tru = tk.Button(root, text="Trừ", command=tru_ma_tran_handle)
btn_tru.pack(padx=10, pady=10)

# Nút nhân hai ma trận
btn_nhan = tk.Button(root, text="Nhân", command=nhan_ma_tran_handle)
btn_nhan.pack(padx=10, pady=10)

# Nút chia hai ma trận
btn_chia = tk.Button(root, text="Chia", command=chia_ma_tran_handle)
btn_chia.pack(padx=10, pady=10)

# Chạy vòng lặp giao diện
root.mainloop()