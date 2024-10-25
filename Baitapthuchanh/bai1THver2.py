import numpy as np
import tkinter as tk
from tkinter import messagebox, filedialog
import csv
def giai_he_phuong_trinh(A, B):
  try:
    nghiem = np.linalg.solve(A, B)
    return nghiem
  except np.linalg.LinAlgError:
    return "Hệ phương trình không có nghiệm duy nhất"
def lay_du_lieu():
  try:
    n = int(entry_n.get())
    A = []
    B = []
    for i in range(n):
      row = []
      for j in range(n):
        row.append(float(entries_A[i][j].get()))
      A.append(row)
      B.append(float(entries_B[i].get()))
    A = np.array(A)
    B = np.array(B)
    nghiem = giai_he_phuong_trinh(A, B)
    messagebox.showinfo("Kết quả", f"Nghiệm của hệ phương trình là: {nghiem}")
  except Exception as e:
    messagebox.showerror("Lỗi", str(e))
def doc_file_csv():
  file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
  if not file_path:
    return
  try:
    with open(file_path, mode='r') as file:
      csv_reader = csv.reader(file)
      rows = list(csv_reader)
      n = len(rows)  # Số phương trình là số dòng trong CSV

      if n == 0:
        raise ValueError("Tệp CSV trống.")
      # Kiểm tra xem dữ liệu trong CSV có đúng định dạng không
      for row in rows:
        if len(row) != n + 1:
          raise ValueError("Dữ liệu trong CSV không đủ hoặc không đúng định dạng.")
      entry_n.delete(0, tk.END)
      entry_n.insert(0, n)
      for widget in frame_entries.winfo_children():
        widget.destroy()
      global entries_A, entries_B
      entries_A = []
      entries_B = []
      tk.Label(frame_entries, text="Ma trận A").grid(row=0, column=0, columnspan=n)
      tk.Label(frame_entries, text="Ma trận B").grid(row=0, column=n)
      for i in range(n):
        row_entries = []
        for j in range(n):
          entry = tk.Entry(frame_entries, width=5)
          entry.grid(row=i + 1, column=j)
          entry.insert(0, rows[i][j])
          row_entries.append(entry)
        entries_A.append(row_entries)
        entry_b = tk.Entry(frame_entries, width=5)
        entry_b.grid(row=i + 1, column=n)
        entry_b.insert(0, rows[i][n])
        entries_B.append(entry_b)
  except Exception as e:
    messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi đọc file CSV: {e}")
def tao_giao_dien():
  global entries_A, entries_B, entry_n, frame_entries
  window = tk.Tk()
  window.title("Giải hệ phương trình tuyến tính")
  tk.Label(window, text="Nhập số ẩn (n):").grid(row=0, column=0)
  entry_n = tk.Entry(window)
  entry_n.grid(row=0, column=1)
  def create_entries():
    try:
      n = int(entry_n.get())
      for widget in frame_entries.winfo_children():
        widget.destroy()
      global entries_A, entries_B
      entries_A = []
      entries_B = []
      tk.Label(frame_entries, text="Ma trận A").grid(row=0, column=0, columnspan=n)
      tk.Label(frame_entries, text="Ma trận B").grid(row=0, column=n)
      for i in range(n):
        row_entries = []
        for j in range(n):
          entry = tk.Entry(frame_entries, width=5)
          entry.grid(row=i + 1, column=j)
          row_entries.append(entry)
        entries_A.append(row_entries)
        entry_b = tk.Entry(frame_entries, width=5)
        entry_b.grid(row=i + 1, column=n)
        entries_B.append(entry_b)
    except Exception as e:
      messagebox.showerror("Lỗi", "Du lieu nhap sai hoac khong co du lieu")
  btn_create_entries = tk.Button(window, text="Tạo ô nhập liệu", command=create_entries)
  btn_create_entries.grid(row=1, column=0, columnspan=2)
  btn_load_csv = tk.Button(window, text="Nhập từ CSV", command=doc_file_csv)
  btn_load_csv.grid(row=2, column=0, columnspan=2)
  frame_entries = tk.Frame(window)
  frame_entries.grid(row=3, column=0, columnspan=2)
  btn1 = tk.Button(window, text="Giải hệ phương trình", command=lay_du_lieu)
  btn1.grid(row=4, column=0, columnspan=2)
  window.mainloop()
tao_giao_dien()
