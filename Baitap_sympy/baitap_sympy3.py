import tkinter as tk
from tkinter import ttk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


# --- Hàm xử lý ---
def clear_output():
    for widget in output_frame.winfo_children():
        widget.destroy()


def solve_linear_equation():
    clear_output()
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        if a == 0:
            if b == 0:
                result = "Phương trình có vô số nghiệm"
            else:
                result = "Phương trình vô nghiệm"
        else:
            x = -b / a
            result = f"Nghiệm của phương trình là x = {x}"
    except ValueError:
        result = "Đầu vào không hợp lệ. Vui lòng nhập số."
    show_result(result)


def solve_quadratic_equation():
    clear_output()
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        c = float(entry_c.get())
        delta = b ** 2 - 4 * a * c
        if delta < 0:
            result = "Phương trình vô nghiệm"
        elif delta == 0:
            x = -b / (2 * a)
            result = f"Phương trình có nghiệm kép x1 = x2 = {x}"
        else:
            x1 = (-b + delta ** 0.5) / (2 * a)
            x2 = (-b - delta ** 0.5) / (2 * a)
            result = f"Phương trình có 2 nghiệm phân biệt: x1 = {x1}, x2 = {x2}"
    except ValueError:
        result = "Đầu vào không hợp lệ. Vui lòng nhập số."
    show_result(result)


def solve_linear_system():
    clear_output()
    try:
        a1 = float(entry_a1.get())
        b1 = float(entry_b1.get())
        c1 = float(entry_c1.get())
        a2 = float(entry_a2.get())
        b2 = float(entry_b2.get())
        c2 = float(entry_c2.get())

        D = a1 * b2 - a2 * b1
        Dx = c1 * b2 - c2 * b1
        Dy = a1 * c2 - a2 * c1

        if D == 0:
            if Dx == 0 and Dy == 0:
                result = "Hệ phương trình có vô số nghiệm"
            else:
                result = "Hệ phương trình vô nghiệm"
        else:
            x = Dx / D
            y = Dy / D
            result = f"Nghiệm của hệ phương trình là: x = {x}, y = {y}"

    except ValueError:
        result = "Đầu vào không hợp lệ. Vui lòng nhập số."
    show_result(result)


def create_matrix_entries():
    global matrix_entries
    try:
        rows = int(entry_rows.get())
        cols = int(entry_cols.get())
    except ValueError:
        show_result("Kích thước ma trận không hợp lệ.")
        return

    for widget in matrix_frame.winfo_children():
        widget.destroy()

    matrix_entries = []
    for i in range(rows):
        row_entries = []
        for j in range(cols):
            entry = tk.Entry(matrix_frame, width=5)
            entry.grid(row=i, column=j, padx=5, pady=5)
            row_entries.append(entry)
        matrix_entries.append(row_entries)


def get_matrix_from_entries():
    try:
        rows = int(entry_rows.get())
        cols = int(entry_cols.get())
        matrix = []
        for i in range(rows):
            row = []
            for j in range(cols):
                value = float(matrix_entries[i][j].get())
                row.append(value)
            matrix.append(row)
        return np.array(matrix)
    except ValueError:
        show_result("Giá trị trong ma trận không hợp lệ.")
        return None


def find_inverse_matrix():
    clear_output()
    matrix = get_matrix_from_entries()
    if matrix is not None:
        try:
            inverse_matrix = np.linalg.inv(matrix)
            result = f"Ma trận nghịch đảo là:\n{inverse_matrix}"
        except np.linalg.LinAlgError:
            result = "Ma trận không khả nghịch"
        show_result(result)


def calculate_determinant():
    clear_output()
    matrix = get_matrix_from_entries()
    if matrix is not None:
        try:
            determinant = np.linalg.det(matrix)
            result = f"Định thức của ma trận là: {determinant}"
        except np.linalg.LinAlgError:
            result = "Không thể tính định thức của ma trận không vuông."
        show_result(result)


def show_result(result):
    result_label = tk.Label(output_frame, text=result, font=("Arial", 14), wraplength=500)
    result_label.pack(pady=10)


# --- Giao diện đồ họa ---
window = tk.Tk()
window.title("Ứng dụng Hỗ trợ Đại số")
window.configure(bg="lightblue")

# --- Frame chính ---
main_frame = tk.Frame(window, bg="lightblue")
main_frame.pack(pady=20, padx=20)

# --- Frame chứa các button ---
button_frame = tk.Frame(main_frame, bg="lightblue")
button_frame.grid(row=0, column=0, rowspan=6, padx=20, sticky="n")

# --- Các button chức năng ---
btn_linear_eq = tk.Button(button_frame, text="Giải phương trình bậc nhất", command=solve_linear_equation, width=25)
btn_linear_eq.grid(row=0, column=0, pady=5)
btn_quadratic_eq = tk.Button(button_frame, text="Giải phương trình bậc hai", command=solve_quadratic_equation, width=25)
btn_quadratic_eq.grid(row=1, column=0, pady=5)
btn_linear_system = tk.Button(button_frame, text="Giải hệ phương trình", command=solve_linear_system, width=25)
btn_linear_system.grid(row=2, column=0, pady=5)
btn_inverse_matrix = tk.Button(button_frame, text="Tìm ma trận nghịch đảo", command=find_inverse_matrix, width=25)
btn_inverse_matrix.grid(row=3, column=0, pady=5)
btn_determinant = tk.Button(button_frame, text="Tính định thức ma trận", command=calculate_determinant, width=25)
btn_determinant.grid(row=4, column=0, pady=5)

# --- Frame chứa input ---
input_frame = tk.Frame(main_frame, bg="lightblue")
input_frame.grid(row=0, column=1, sticky="nw")

# --- Input cho phương trình bậc nhất ---
label_a = tk.Label(input_frame, text="Nhập a:", bg="lightblue")
label_a.grid(row=0, column=0)
entry_a = tk.Entry(input_frame)
entry_a.grid(row=0, column=1)
label_b = tk.Label(input_frame, text="Nhập b:", bg="lightblue")
label_b.grid(row=0, column=2)
entry_b = tk.Entry(input_frame)
entry_b.grid(row=0, column=3)

# --- Input cho phương trình bậc hai ---
label_c = tk.Label(input_frame, text="Nhập c:", bg="lightblue")
label_c.grid(row=1, column=2)
entry_c = tk.Entry(input_frame)
entry_c.grid(row=1, column=3)

# --- Input cho hệ phương trình ---
label_a1 = tk.Label(input_frame, text="a1:", bg="lightblue")
label_a1.grid(row=2, column=0)
entry_a1 = tk.Entry(input_frame, width=5)
entry_a1.grid(row=2, column=1)
label_b1 = tk.Label(input_frame, text="b1:", bg="lightblue")
label_b1.grid(row=2, column=2)
entry_b1 = tk.Entry(input_frame, width=5)
entry_b1.grid(row=2, column=3)
label_c1 = tk.Label(input_frame, text="c1:", bg="lightblue")
label_c1.grid(row=2, column=4)
entry_c1 = tk.Entry(input_frame, width=5)
entry_c1.grid(row=2, column=5)

label_a2 = tk.Label(input_frame, text="a2:", bg="lightblue")
label_a2.grid(row=3, column=0)
entry_a2 = tk.Entry(input_frame, width=5)
entry_a2.grid(row=3, column=1)
label_b2 = tk.Label(input_frame, text="b2:", bg="lightblue")
label_b2.grid(row=3, column=2)
entry_b2 = tk.Entry(input_frame, width=5)
entry_b2.grid(row=3, column=3)
label_c2 = tk.Label(input_frame, text="c2:", bg="lightblue")
label_c2.grid(row=3, column=4)
entry_c2 = tk.Entry(input_frame, width=5)
entry_c2.grid(row=3, column=5)

# --- Khung nhập ma trận ---
matrix_input_frame = tk.Frame(main_frame, bg="lightblue")
matrix_input_frame.grid(row=4, column=1, sticky="nw")

label_rows = tk.Label(matrix_input_frame, text="Số hàng:", bg="lightblue")
label_rows.grid(row=0, column=0)
entry_rows = tk.Entry(matrix_input_frame, width=5)
entry_rows.grid(row=0, column=1)
label_cols = tk.Label(matrix_input_frame, text="Số cột:", bg="lightblue")
label_cols.grid(row=0, column=2)
entry_cols = tk.Entry(matrix_input_frame, width=5)
entry_cols.grid(row=0, column=3)
create_matrix_button = tk.Button(matrix_input_frame, text="Tạo ma trận", command=create_matrix_entries)
create_matrix_button.grid(row=0, column=4)

# --- Frame chứa các phần tử ma trận ---
matrix_frame = tk.Frame(main_frame, bg="lightblue")
matrix_frame.grid(row=5, column=1, sticky="nw")

# --- Frame chứa output ---
output_frame = tk.Frame(main_frame, bg="lightblue")
output_frame.grid(row=6, column=0, columnspan=2, sticky="nw")

window.mainloop()