import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from itertools import product, combinations
import csv

# Functions to plot 2D shapes
def plot_circle(radius):
    theta = np.linspace(0, 2 * np.pi, 300)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    plt.figure()
    plt.plot(x, y)
    plt.axis('equal')
    plt.title(f'Đồ thị hình tròn bán kính {radius}')
    plt.show()

def plot_square(side):
    plt.figure()
    square = plt.Rectangle((0, 0), side, side, fill=None, edgecolor='r')
    plt.gca().add_patch(square)
    plt.axis('equal')
    plt.title(f'Đồ thị hình vuông cạnh {side}')
    plt.show()

def plot_rectangle(length, width):
    plt.figure()
    rectangle = plt.Rectangle((0, 0), length, width, fill=None, edgecolor='b')
    plt.gca().add_patch(rectangle)
    plt.axis('equal')
    plt.title(f'Đồ thị hình chữ nhật {length}x{width}')
    plt.show()

def plot_hexagon(side):
    theta = np.linspace(0, 2 * np.pi, 7)
    x = side * np.cos(theta)
    y = side * np.sin(theta)
    plt.figure()
    plt.plot(x, y)
    plt.axis('equal')
    plt.title(f'Đồ thị hình lục giác cạnh {side}')
    plt.show()

# Functions to plot 3D shapes
def plot_sphere(radius):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = radius * np.outer(np.cos(u), np.sin(v))
    y = radius * np.outer(np.sin(u), np.sin(v))
    z = radius * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z, color='b')
    plt.title(f'Đồ thị hình cầu bán kính {radius}')
    plt.show()

def plot_cube(side):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    r = [-side/2, side/2]
    for s, e in combinations(np.array(list(product(r, r, r))), 2):
        if np.sum(np.abs(s - e)) == r[1] - r[0]:
            ax.plot3D(*zip(s, e), color="r")
    plt.title(f'Đồ thị hình lập phương cạnh {side}')
    plt.show()

def plot_cylinder(radius, height):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = np.linspace(-radius, radius, 100)
    z = np.linspace(0, height, 100)
    Xc, Zc = np.meshgrid(x, z)
    Yc = np.sqrt(radius**2 - Xc**2)
    ax.plot_surface(Xc, Yc, Zc, alpha=0.5, rstride=100, cstride=100)
    ax.plot_surface(Xc, -Yc, Zc, alpha=0.5, rstride=100, cstride=100)
    plt.title(f'Đồ thị hình trụ')
    plt.show()

# Function to read CSV and plot data
def plot_csv_data(file_path):
    try:
        data = np.genfromtxt(file_path, delimiter=',', skip_header=1)
        if data.size == 0:
            raise ValueError("CSV file is empty.")

        if data.shape[1] == 2:
            plt.plot(data[:, 0], data[:, 1], 'o-')
            plt.title('Đồ thị từ dữ liệu CSV')
            plt.show()
        elif data.shape[1] == 3:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.plot(data[:, 0], data[:, 1], data[:, 2], 'o-')
            plt.title('Đồ thị 3D từ dữ liệu CSV')
            plt.show()
        else:
            raise ValueError("Dữ liệu CSV không hợp lệ. Phải có 2 hoặc 3 cột.")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
def open_tl():
    messagebox.showinfo("Tài liệu Hình học",
                        "Chào mừng bạn đến với tài liệu về hình học! \n\n1. Hình tròn: Là một hình phẳng với các điểm cách đều một điểm gọi là tâm. Công thức: C = 2πr, A = πr².\n\n2. Hình vuông: Là hình có 4 cạnh bằng nhau và 4 góc vuông. Công thức: C = 4a, A = a².\n\n3. Hình chữ nhật: Là hình có 4 cạnh, với 2 cạnh đối diện bằng nhau và 4 góc vuông. Công thức: C = 2(a + b), A = ab.\n\n")
def open_csv_window():
    file_path = filedialog.askopenfilename()
    if file_path:
        plot_csv_data(file_path)

# Functions to open windows for inputs
def open_circle_window():
    win = tk.Toplevel(app)
    tk.Label(win, text="Nhập bán kính:").pack()
    radius_entry = tk.Entry(win)
    radius_entry.pack()
    tk.Button(win, text="Vẽ", command=lambda: plot_circle(float(radius_entry.get()))).pack()

def open_square_window():
    win = tk.Toplevel(app)
    tk.Label(win, text="Nhập cạnh:").pack()
    side_entry = tk.Entry(win)
    side_entry.pack()
    tk.Button(win, text="Vẽ", command=lambda: plot_square(float(side_entry.get()))).pack()

def open_rectangle_window():
    win = tk.Toplevel(app)
    tk.Label(win, text="Nhập chiều dài:").pack()
    length_entry = tk.Entry(win)
    length_entry.pack()
    tk.Label(win, text="Nhập chiều rộng:").pack()
    width_entry = tk.Entry(win)
    width_entry.pack()
    tk.Button(win, text="Vẽ", command=lambda: plot_rectangle(float(length_entry.get()), float(width_entry.get()))).pack()

def open_hexagon_window():
    win = tk.Toplevel(app)
    tk.Label(win, text="Nhập cạnh:").pack()
    side_entry = tk.Entry(win)
    side_entry.pack()
    tk.Button(win, text="Vẽ", command=lambda: plot_hexagon(float(side_entry.get()))).pack()

def open_sphere_window():
    win = tk.Toplevel(app)
    tk.Label(win, text="Nhập bán kính:").pack()
    radius_entry = tk.Entry(win)
    radius_entry.pack()
    tk.Button(win, text="Vẽ", command=lambda: plot_sphere(float(radius_entry.get()))).pack()

def open_cube_window():
    win = tk.Toplevel(app)
    tk.Label(win, text="Nhập cạnh:").pack()
    side_entry = tk.Entry(win)
    side_entry.pack()
    tk.Button(win, text="Vẽ", command=lambda: plot_cube(float(side_entry.get()))).pack()

def open_cylinder_window():
    win = tk.Toplevel(app)
    tk.Label(win, text="Nhập bán kính:").pack()
    radius_entry = tk.Entry(win)
    radius_entry.pack()
    tk.Label(win, text="Nhập chiều cao:").pack()
    height_entry = tk.Entry(win)
    height_entry.pack()
    tk.Button(win, text="Vẽ", command=lambda: plot_cylinder(float(radius_entry.get()), float(height_entry.get()))).pack()

# Main window with 2D and 3D options
app = tk.Tk()
app.title('Hỗ trợ học tập môn Hình học')

tk.Label(app, text="Chọn loại hình để vẽ:").pack()

frame_2d = tk.Frame(app)
frame_2d.pack(pady=5)
tk.Label(frame_2d, text="2D Shapes").pack()
tk.Button(frame_2d, text="Vẽ hình tròn", command=open_circle_window).pack(pady=2)
tk.Button(frame_2d, text="Vẽ hình vuông", command=open_square_window).pack(pady=2)
tk.Button(frame_2d, text="Vẽ hình chữ nhật", command=open_rectangle_window).pack(pady=2)
tk.Button(frame_2d, text="Vẽ hình lục giác", command=open_hexagon_window).pack(pady=2)

frame_3d = tk.Frame(app)
frame_3d.pack(pady=5)
tk.Label(frame_3d, text="3D Shapes").pack()
tk.Button(frame_3d, text="Vẽ hình cầu", command=open_sphere_window).pack(pady=2)
tk.Button(frame_3d, text="Vẽ hình lập phương", command=open_cube_window).pack(pady=2)
tk.Button(frame_3d, text="Vẽ hình trụ", command=open_cylinder_window).pack(pady=2)

tk.Label(app, text="Hoặc chọn file CSV để nhập dữ liệu:").pack()
tk.Button(app, text="Tai Lieu Hinh học", command=open_tl).pack(pady=5)
tk.Button(app, text="Chọn file CSV", command=open_csv_window).pack(pady=6)

app.mainloop()
