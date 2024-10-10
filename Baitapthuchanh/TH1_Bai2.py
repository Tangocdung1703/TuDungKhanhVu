import sympy
import tkinter as tk
from tkinter import ttk
import os
from sympy.parsing.mathematica import parse_mathematica
from tkinter import scrolledtext
window = tk.Tk()
window.title("Ứng dụng giải tích")
icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
window.iconbitmap(icon_path) # Thêm biểu tượng cho cửa sổ

# Tạo Notebook để quản lý các tab
notebook = ttk.Notebook(window)
# Tạo các tab
tab_Analysis = tk.Frame(notebook)
tab_Geometry = tk.Frame(notebook)
tab_Graph = tk.Frame(notebook)
tab_History = tk.Frame(notebook)
# Thêm các tab 
notebook.add(tab_Analysis, text="Giải tích")
notebook.add(tab_Geometry, text="Hình học")
notebook.add(tab_Graph, text="Đồ thị")
notebook.add(tab_History, text="Các phép toán đã thực hiện")
notebook.pack(expand=True, fill="both")  # Mở rộng Notebook để lấp đầy cửa sổ

#
#
#
# Cửa sổ giải tích
# Hàm kiểm tra đầu vào có phải là số thực?
def validate_input(input):
  """Kiểm tra xem đầu vào có phải là số hay không."""
  if input == "":  # Cho phép ô trống
    return True
  try:
    float(input)
    return True
  except ValueError:
    return False

label_function = tk.Label(tab_Analysis, text="Hàm số: ")
label_function.pack()

entry_function = scrolledtext.ScrolledText(tab_Analysis, wrap=tk.WORD, width=50, height=2)
entry_function.pack()

label_limit_point = tk.Label(tab_Analysis, text="Điểm giới hạn")
label_limit_point.pack()
vcmd = (tab_Analysis.register(validate_input), '%P')  # %P là giá trị mới sau khi nhập
entry_limit_point = tk.Entry(tab_Analysis, validate="key", validatecommand=vcmd)
entry_limit_point.pack()


# Hàm tìm biến
def find_variables(expression_string):
  """Tìm các biến được sử dụng trong biểu thức."""
  expression = parse_mathematica(expression_string)
  variables = expression.free_symbols
  variables = str(variables)
  variables = variables[1:-1]
  return variables

def tinh_gioi_han():
    display_result.delete("1.0", tk.END)
    ham_so_str = entry_function.get("1.0", tk.END)
    bien_str = find_variables(ham_so_str)
    print(f"Biến trong hàm số",bien_str)
    diem_gioi_han = float(entry_limit_point.get())
    try:
        # Chuyển đổi chuỗi thành biểu thức sympy
        bien = sympy.Symbol(bien_str)
        ham_so = parse_mathematica(ham_so_str)
        # Tính giới hạn
        gioi_han = sympy.limit(ham_so, bien, diem_gioi_han)
        # Lưu lại
        #luu_lich_su("Giới hạn", ham_so_str, diem_gioi_han, gioi_han)

        display_result.insert(tk.END, str(gioi_han))
        return gioi_han
        
    except Exception as e:
        print(f"Lỗi khi tính giới hạn: {e}")
        return None

button_result = tk.Button(tab_Analysis, text="Kết quả", command=tinh_gioi_han)
button_result.pack()
display_result = scrolledtext.ScrolledText(tab_Analysis, wrap=tk.WORD, width=50, height=10)
display_result.pack()


# def tinh_dao_ham():
#     # ... (code tính đạo hàm)
#     luu_lich_su("Đạo hàm", ham_so, bien, ket_qua)

# def tinh_tich_phan():
#     # ... (code tính tích phân)
#     luu_lich_su("Tích phân", ham_so, can_duoi, can_tren, ket_qua)

# def tinh_vi_phan():
#     # ... (code tính vi phân)
#     luu_lich_su("Vi phân", ham_so, bien, ket_qua)

# def menu_giai_tich():
#     while True:
#         print("\nChức năng tính toán giải tích")
#         print("1. Giới hạn")
#         print("2. Đạo hàm")
#         print("3. Tích phân")
#         print("4. Vi phân")
#         print("5. Quay lại")

#         lua_chon = input("Chọn chức năng (1-5): ")

#         if lua_chon == "1":
#             tinh_gioi_han()
#         elif lua_chon == "2":
#             tinh_dao_ham()
#         elif lua_chon == "3":
#             tinh_tich_phan()
#         elif lua_chon == "4":
#             tinh_vi_phan()
#         elif lua_chon == "5":
#             break
#         else:
#             print("Lựa chọn không hợp lệ.")



# import sympy
# import lich_su

# def tinh_do_dai_duong_cong():
#     # ... (code tính độ dài đường cong)
#     lich_su.luu_lich_su("Độ dài đường cong", ham_so, can_duoi, can_tren, ket_qua)

# def tinh_dien_tich_be_mat():
#     # ... (code tính diện tích bề mặt)
#     lich_su.luu_lich_su("Diện tích bề mặt", ham_so, mien_tich_phan, ket_qua)

# def tinh_the_tich():
#     # ... (code tính thể tích)
#     lich_su.luu_lich_su("Thể tích", ham_so, mien_tich_phan, ket_qua)

# def menu_hinh_hoc():
#     # ... (tương tự menu_giai_tich)
#     pass




# import matplotlib.pyplot as plt
# import mpl_toolkits.mplot3d as a3
# import sympy

# def ve_do_thi_2d():
#     # ... (code vẽ đồ thị 2D)
#     pass

# def ve_do_thi_3d():
#     # ... (code vẽ đồ thị 3D)
#     pass

# def menu_do_thi():
#     # ... (tương tự menu_giai_tich)
#     pass

















# import json
# import os

# LICH_SU_FILE = "lich_su.json"

# def luu_lich_su(loai_phep_toan, *args):
#     try:
#         with open(LICH_SU_FILE, "r") as f:
#             lich_su = json.load(f)
#     except FileNotFoundError:
#         lich_su = []
#     lich_su.append({"loai": loai_phep_toan, "args": args})
#     with open(LICH_SU_FILE, "w") as f:
#         json.dump(lich_su, f, indent=4)

# def xem_lich_su():
#     try:
#         with open(LICH_SU_FILE, "r") as f:
#             lich_su = json.load(f)
#     except FileNotFoundError:
#         print("Lịch sử trống.")
#         return
#     print("\nLịch sử tính toán:")
#     for i, entry in enumerate(lich_su):
#         print(f"{i+1}. {entry['loai']}: {entry['args']}")

# def xoa_lich_su():
#     if os.path.exists(LICH_SU_FILE):
#         os.remove(LICH_SU_FILE)
#         print("Lịch sử đã được xóa.")
#     else:
#         print("Lịch sử trống.")






















# while True:
#     print("\nỨng dụng hỗ trợ môn học Giải tích")
#     print("1. Tính toán giải tích")
#     print("2. Tính toán hình học")
#     print("3. Vẽ đồ thị hàm số")
#     print("4. Xem lịch sử")
#     print("5. Thoát")

#     lua_chon = input("Chọn chức năng (1-5): ")

#     if lua_chon == "1":
#         giai_tich.menu_giai_tich()
#     elif lua_chon == "2":
#         hinh_hoc.menu_hinh_hoc()
#     elif lua_chon == "3":
#         do_thi.menu_do_thi()
#     elif lua_chon == "4":
#         lich_su.xem_lich_su()
#     elif lua_chon == "5":
#         break
#     else:
#         print("Lựa chọn không hợp lệ.")

window.mainloop()