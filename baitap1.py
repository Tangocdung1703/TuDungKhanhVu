import numpy as np
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Import ttk cho widget hiện đại hơn

# --- Hàm xử lý ---
def giai_he_pt(A, B):
    try:
        A_inv = np.linalg.inv(A)
        X = np.dot(A_inv, B)
        return X
    except np.linalg.LinAlgError:
        return None

def solve_system():
    try:
        n = int(entry_n.get())
        A = np.zeros((n, n))
        B = np.zeros(n)

        for i in range(n):
            for j in range(n):
                A[i, j] = float(entries_A[i][j].get())
            B[i] = float(entries_B[i].get())

        result = giai_he_pt(A, B)
        if result is None:
            messagebox.showerror("Lỗi", "Hệ phương trình không có nghiệm hoặc vô số nghiệm")
        else:
            result_str = ', '.join([f"x{i + 1} = {result[i]:.2f}" for i in range(n)])
            messagebox.showinfo("Kết quả", f"Nghiệm của hệ là:\n{result_str}")
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ")

def create_input_fields():
    try:
        n = int(entry_n.get())
        for widget in frame_inputs.winfo_children():
            widget.destroy()

        global entries_A, entries_B
        entries_A = []
        entries_B = []

        # Tạo label "Ma trận A" và "Ma trận B"
        label_matrix_a = tk.Label(frame_inputs, text="Ma trận A:", font=("Arial", 12))
        label_matrix_a.grid(row=0, column=0, columnspan=n, pady=(10, 5))
        label_matrix_b = tk.Label(frame_inputs, text="Ma trận B:", font=("Arial", 12))
        label_matrix_b.grid(row=0, column=n, pady=(10, 5))

        for i in range(n):
            row_entries = []
            for j in range(n):
                cell_frame_a = tk.Frame(frame_inputs)
                cell_frame_a.grid(row=i + 1, column=j, padx=5, pady=5)

                entry_a = tk.Entry(cell_frame_a, width=5, font=("Arial", 12))
                entry_a.pack(side="left")

                row_entries.append(entry_a)
            entries_A.append(row_entries)

        for i in range(n):
            cell_frame_b = tk.Frame(frame_inputs)
            cell_frame_b.grid(row=i + 1, column=n, padx=5, pady=5)

            entry_b = tk.Entry(cell_frame_b, width=5, font=("Arial", 12))
            entry_b.pack(side="left")

            entries_B.append(entry_b)

    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số phương trình hợp lệ")

# --- Giao diện ---
root = tk.Tk()
root.title("Giải hệ phương trình tuyến tính")
# Thiết lập style cho button
style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#ccc", font=("Arial", 12))

frame_top = tk.Frame(root)
frame_top.pack(padx=20, pady=20)

label_n = tk.Label(frame_top, text="Số phương trình và số ẩn:", font=("Arial", 12))
label_n.pack(side=tk.LEFT)

entry_n = tk.Entry(frame_top, width=5, font=("Arial", 12))
entry_n.pack(side=tk.LEFT, padx=5)

btn_create_fields = ttk.Button(frame_top, text="Tạo", command=create_input_fields)
btn_create_fields.pack(side=tk.LEFT, padx=5)

frame_inputs = tk.Frame(root)
frame_inputs.pack(padx=20, pady=(0, 20))

btn_solve = ttk.Button(root, text="Giải", command=solve_system)
btn_solve.pack()

root.mainloop()