import tkinter as tk
from tkinter import messagebox, filedialog
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import csv

def solve():
  equation = entry_equation.get()
  if equation:
    result = solve_equation(equation)
    result_label.config(text=f'Kết quả: {result}')
  else:
    messagebox.showwarning("Cảnh báo", "Vui lòng nhập phương trình!")


def integrate():
  function = entry_integrate.get()
  if function:
    result = integrate_function(function)
    result_label.config(text=f'Tích phân: {result}')
  else:
    messagebox.showwarning("Cảnh báo", "Vui lòng nhập hàm số!")


def plot():
  function = entry_plot.get()
  if function:
    plot_function(function)
  else:
    messagebox.showwarning("Cảnh báo", "Vui lòng nhập hàm số!")
# Define functions to perform mathematical operations
def solve_equation(equation):
  try:
    x = sp.symbols('x')
    eq = sp.sympify(equation)
    solutions = sp.solve(eq, x)
    return solutions
  except Exception as e:
    return f"Lỗi: {e}"


def integrate_function(function):
  try:
    x = sp.symbols('x')
    result = sp.integrate(sp.sympify(function), x)
    return result
  except Exception as e:
    return f"Lỗi: {e}"


def plot_function(function):
  try:
    x = sp.symbols('x')
    expr = sp.sympify(function)
    f = sp.lambdify(x, expr, modules=['numpy'])
    x_vals = np.linspace(-10, 10, 400)
    y_vals = f(x_vals)
    plt.plot(x_vals, y_vals)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f'Đồ thị của {function}')
    plt.grid(True)
    plt.show()
  except Exception as e:
    messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi vẽ đồ thị: {e}")


# Content for documents and quizzes
CONTENT = {'docs': {'Derivatives': 'Đạo hàm của một hàm số...', 'Integrals': 'Tích phân của một hàm số...'},
  'quizzes': {'Quiz 1': {'question': 'Tính đạo hàm của x^2 + 3x + 2', 'answer': '2*x + 3'}}}


# Function to perform operations based on CSV content
def perform_operations(headers, data):
  results = []
  if 'Equation' in headers:
    for row in data:
      equation = row[0]
      result = solve_equation(equation)
      results.append((equation, result))
  elif 'Function' in headers:
    for row in data:
      function = row[0]
      result = integrate_function(function)
      results.append((function, result))
      plot_function(function)
  return results


# Functions to handle CSV data
def read_csv(file_path):
  try:
    data = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
      reader = csv.reader(csvfile)
      headers = next(reader)
      for row in reader:
        data.append(row)
    return headers, data
  except Exception as e:
    messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi đọc file CSV: {e}")
    return None, None


def display_csv_data(headers, data, results):
  csv_window = tk.Toplevel(app)
  csv_window.title('Dữ liệu CSV')

  for i, header in enumerate(headers):
    tk.Label(csv_window, text=header).grid(row=0, column=i)

  for i, row in enumerate(data):
    for j, value in enumerate(row):
      tk.Label(csv_window, text=value).grid(row=i + 1, column=j)

  tk.Label(csv_window, text='Kết quả').grid(row=0, column=len(headers))

  for i, (input_value, result) in enumerate(results):
    tk.Label(csv_window, text=str(result)).grid(row=i + 1, column=len(headers))


def open_csv_file():
  file_path = filedialog.askopenfilename()
  if file_path:
    headers, data = read_csv(file_path)
    if headers and data:
      results = perform_operations(headers, data)
      display_csv_data(headers, data, results)


# Functions to open specific windows for operations
def open_solve_window():
  solve_window = tk.Toplevel(app)
  solve_window.title('Giải phương trình')
  tk.Label(solve_window, text='Giải phương trình:').pack()
  global entry_equation
  entry_equation = tk.Entry(solve_window)
  entry_equation.pack()
  tk.Button(solve_window, text='Giải', command=solve).pack()
  global result_label
  result_label = tk.Label(solve_window, text='')
  result_label.pack()


def open_integrate_window():
  integrate_window = tk.Toplevel(app)
  integrate_window.title('Tính tích phân')
  tk.Label(integrate_window, text='Tính tích phân:').pack()
  global entry_integrate
  entry_integrate = tk.Entry(integrate_window)
  entry_integrate.pack()
  tk.Button(integrate_window, text='Tính', command=integrate).pack()
  global result_label
  result_label = tk.Label(integrate_window, text='')
  result_label.pack()


def open_plot_window():
  plot_window = tk.Toplevel(app)
  plot_window.title('Vẽ đồ thị')
  tk.Label(plot_window, text='Vẽ đồ thị:').pack()
  global entry_plot
  entry_plot = tk.Entry(plot_window)
  entry_plot.pack()
  tk.Button(plot_window, text='Vẽ', command=plot).pack()


def show_document(doc_key):
  content = CONTENT['docs'].get(doc_key, 'Không tìm thấy tài liệu.')
  messagebox.showinfo("Tài liệu học tập", content)


def check_quiz(quiz_key):
  answer = entry_quiz.get()
  correct_answer = CONTENT['quizzes'][quiz_key]['answer']
  if answer == correct_answer:
    messagebox.showinfo("Kết quả", "Chính xác!")
  else:
    messagebox.showinfo("Kết quả", f"Sai. Đáp án đúng là: {correct_answer}")


def open_docs_window():
  docs_window = tk.Toplevel(app)
  docs_window.title('Tài liệu học tập')
  tk.Label(docs_window, text='Tài liệu học tập:').pack()
  for doc_key in CONTENT['docs'].keys():
    tk.Button(docs_window, text=doc_key, command=lambda key=doc_key: show_document(key)).pack()


def open_quiz_window():
  quiz_window = tk.Toplevel(app)
  quiz_window.title('Kiểm tra kiến thức')
  tk.Label(quiz_window, text='Kiểm tra kiến thức:').pack()
  global entry_quiz
  quiz_key = list(CONTENT['quizzes'].keys())[0]
  tk.Label(quiz_window, text=CONTENT['quizzes'][quiz_key]['question']).pack()
  entry_quiz = tk.Entry(quiz_window)
  entry_quiz.pack()
  tk.Button(quiz_window, text='Kiểm tra', command=lambda key=quiz_key: check_quiz(key)).pack()


def show_csv_instructions():
  instructions = ("Hướng dẫn nhập dữ liệu từ file CSV:\n\n"
                  "1. Tạo file CSV với các cột tương ứng.\n"
                  "   - Giải phương trình: Tạo file equations.csv với 1 cột 'Equation'.\n"
                  "   - Tính tích phân: Tạo file functions.csv với 1 cột 'Function'.\n"
                  "   - Vẽ đồ thị: Tạo file plot_functions.csv với 1 cột 'Function'.\n\n"
                  "2. Đảm bảo rằng mỗi hàng chứa một phương trình hoặc hàm số tương ứng.\n\n"
                  "Ví dụ cho file equations.csv:\n"
                  "Equation\n"
                  "x**2 - 4\n"
                  "x**2 + 5*x + 6\n\n"
                  "Ví dụ cho file functions.csv hoặc plot_functions.csv:\n"
                  "Function\n"
                  "x**2\n"
                  "x**3 + x**2 + x\n")
  messagebox.showinfo("Hướng dẫn CSV", instructions)


# Define the main application window
app = tk.Tk()
app.title('Hỗ trợ học tập môn Giải tích')

# Add buttons for each feature
tk.Button(app, text='Giải phương trình', command=open_solve_window).pack()
tk.Button(app, text='Tính tích phân', command=open_integrate_window).pack()
tk.Button(app, text='Vẽ đồ thị', command=open_plot_window).pack()
tk.Button(app, text='Tài liệu học tập', command=open_docs_window).pack()
tk.Button(app, text='Kiểm tra kiến thức', command=open_quiz_window).pack()
tk.Button(app, text='Hướng dẫn nhập file CSV', command=show_csv_instructions).pack()
tk.Button(app, text='Nhập dữ liệu CSV', command=open_csv_file).pack()

# Run the main loop
app.mainloop()
