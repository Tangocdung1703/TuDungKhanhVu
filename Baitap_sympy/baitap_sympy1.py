import sympy as sym
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from sympy.parsing.mathematica import parse_mathematica

def get_expression():
    """Lấy biểu thức từ ô nhập liệu và kiểm tra tính hợp lệ."""
    expr_str = expr_entry.get()
    try:
        expr = parse_mathematica(expr_str)
        return expr
    except:
        result_label.config(text="Lỗi: Biểu thức không hợp lệ.")
        return None

def tinh_cuc_tri():
    expression = get_expression()
    if expression:
        try:
            # Tìm đạo hàm bậc 1
            derivative = sym.diff(expression, x)

            # Tìm nghiệm của đạo hàm bằng cách giải phương trình derivative = 0
            critical_points = sym.solve(derivative, x)

            # Tính đạo hàm bậc 2
            second_derivative = sym.diff(expression, x, 2)

            # Kiểm tra dấu của đạo hàm bậc 2 tại các điểm cực trị
            cuc_dai = []
            cuc_tieu = []
            for point in critical_points:
                if second_derivative.subs(x, point) > 0:
                    cuc_tieu.append(point)
                elif second_derivative.subs(x, point) < 0:
                    cuc_dai.append(point)

            # Hiển thị kết quả
            if cuc_dai:
                result_label.config(text=f"Cực đại tại x = {cuc_dai}")
            if cuc_tieu:
                result_label.config(text=f"Cực tiểu tại x = {cuc_tieu}")
            if not cuc_dai and not cuc_tieu:
                result_label.config(text="Hàm số không có cực trị.")

        except Exception as e:
            result_label.config(text=f"Lỗi tính cực trị: {e}")

def tinh_gioi_han():
    expression = get_expression()
    if expression:
        try:
            target = entry_target.get()
            if target:
                target = float(target)
                limit_value = sym.limit(expression, x, target)
                result_label.config(text=f"Giới hạn của biểu thức khi x tiến đến {target} là: {limit_value}")
            else:
                result_label.config(text="Vui lòng nhập giá trị x tiến đến.")
        except Exception as e:
            result_label.config(text=f"Lỗi tính giới hạn: {e}")

def tinh_dao_ham_rieng():
    expression = get_expression()
    if expression:
        try:
            # Lấy biến cần tính đạo hàm riêng từ người dùng
            variable_str = entry_variable.get()
            if variable_str:
                variable = sym.Symbol(variable_str)
                partial_derivative = sym.diff(expression, variable)
                result_label.config(text=f"Đạo hàm riêng theo {variable} là: {partial_derivative}")
            else:
                result_label.config(text="Vui lòng nhập biến cần tính đạo hàm riêng.")
        except Exception as e:
            result_label.config(text=f"Lỗi tính đạo hàm riêng: {e}")

def calculate_derivative():
    """Tính và hiển thị đạo hàm."""
    expression = get_expression()
    if expression:
        derivative = sym.diff(expression, x)
        result_label.config(text=f"Đạo hàm: {derivative}")

def calculate_integral():
    """Tính và hiển thị tích phân."""
    expression = get_expression()
    if expression:
        try:
            lower_limit = entry_lower_limit.get()
            upper_limit = entry_upper_limit.get()

            if lower_limit and upper_limit:
                lower_limit = float(lower_limit)
                upper_limit = float(upper_limit)
                integral = sym.integrate(expression, (x, lower_limit, upper_limit))
                result_label.config(text=f"Tích phân từ {lower_limit} đến {upper_limit} là: {integral}")
            else:
                result_label.config(text="Vui lòng nhập cả cận trên và cận dưới.")
        except Exception as e:
            result_label.config(text=f"Lỗi tính tích phân: {e}")

def plot_function():
    """Vẽ và hiển thị đồ thị."""
    expression = get_expression()
    if expression:
        x_vals = np.linspace(-10, 10, 200)
        y_vals = sym.lambdify(x, expression, 'numpy')(x_vals)
        ax.clear()
        ax.plot(x_vals, y_vals)
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.grid(True)
        canvas.draw()


# --- Giao diện đồ họa ---

window = tk.Tk()
window.title("Ứng dụng Giải tích")

# Tạo Notebook (tab)
notebook = ttk.Notebook(window)
notebook.pack(expand=True, fill="both")

# --- Tab Nhập biểu thức và kết quả ---
tab_bieu_thuc = ttk.Frame(notebook)
notebook.add(tab_bieu_thuc, text="Biểu thức")

# Biến SymPy
x = sym.Symbol('x')

# Tạo các widget
expr_label = tk.Label(tab_bieu_thuc, text="Nhập biểu thức (ví dụ: x**2 + Sin[x]):")
expr_label.pack(pady=5) 

expr_entry = tk.Entry(tab_bieu_thuc, width=50)
expr_entry.pack(pady=5) 

derivative_button = tk.Button(tab_bieu_thuc, text="Tính Đạo hàm", command=calculate_derivative)
derivative_button.pack(side=tk.LEFT,pady=5, padx=5)

integral_button = tk.Button(tab_bieu_thuc, text="Tính Tích phân", command=calculate_integral)
integral_button.pack(side=tk.LEFT,pady=5, padx=5)

plot_button = tk.Button(tab_bieu_thuc, text="Vẽ Đồ thị", command=plot_function)
plot_button.pack(side=tk.LEFT,pady=5, padx=5)

result_label = tk.Label(tab_bieu_thuc, text="", wraplength=400)
result_label.pack(fill=tk.BOTH, expand=True) 

# Tạo khung vẽ Matplotlib
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=tab_bieu_thuc)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True) 

# --- Tab Giới hạn ---
tab_gioi_han = ttk.Frame(notebook)
notebook.add(tab_gioi_han, text="Giới hạn")

label_target = ttk.Label(tab_gioi_han, text="Nhập giá trị x tiến đến:")
label_target.grid(row=0, column=0, padx=5, pady=5)
entry_target = ttk.Entry(tab_gioi_han)
entry_target.grid(row=0, column=1, padx=5, pady=5)

button_tinh_gioi_han = ttk.Button(tab_gioi_han, text="Tính giới hạn", command=tinh_gioi_han)
button_tinh_gioi_han.grid(row=1, column=0, columnspan=2, pady=10)

# --- Tab Cực trị ---
tab_cuc_tri = ttk.Frame(notebook)
notebook.add(tab_cuc_tri, text="Cực trị")

button_tinh_cuc_tri = ttk.Button(tab_cuc_tri, text="Tìm cực trị", command=tinh_cuc_tri)
button_tinh_cuc_tri.pack(pady=10)

# --- Tab Đạo hàm riêng ---
tab_dao_ham_rieng = ttk.Frame(notebook)
notebook.add(tab_dao_ham_rieng, text="Đạo hàm riêng")

label_variable = ttk.Label(tab_dao_ham_rieng, text="Nhập biến cần tính đạo hàm riêng:")
label_variable.grid(row=0, column=0, padx=5, pady=5)
entry_variable = ttk.Entry(tab_dao_ham_rieng)
entry_variable.grid(row=0, column=1, padx=5, pady=5)

button_tinh_dao_ham_rieng = ttk.Button(tab_dao_ham_rieng, text="Tính đạo hàm riêng", command=tinh_dao_ham_rieng)
button_tinh_dao_ham_rieng.grid(row=1, column=0, columnspan=2, pady=10)

# --- Tab Tích phân ---
tab_tich_phan = ttk.Frame(notebook)
notebook.add(tab_tich_phan, text="Tích phân")

label_lower_limit = ttk.Label(tab_tich_phan, text="Cận dưới:")
label_lower_limit.grid(row=0, column=0, padx=5, pady=5)
entry_lower_limit = ttk.Entry(tab_tich_phan)
entry_lower_limit.grid(row=0, column=1, padx=5, pady=5)

label_upper_limit = ttk.Label(tab_tich_phan, text="Cận trên:")
label_upper_limit.grid(row=1, column=0, padx=5, pady=5)
entry_upper_limit = ttk.Entry(tab_tich_phan)
entry_upper_limit.grid(row=1, column=1, padx=5, pady=5)

button_tinh_tich_phan = ttk.Button(tab_tich_phan, text="Tính tích phân", command=calculate_integral)
button_tinh_tich_phan.grid(row=2, column=0, columnspan=2, pady=10)

window.mainloop()