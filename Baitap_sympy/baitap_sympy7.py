import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy import ndimage

class EdgeDetectionApp:
    def __init__(self, master):
        self.master = master
        master.title("Ứng dụng tách biên ảnh")

        # Khởi tạo biến
        self.original_image = None
        self.edged_image = None

        # Tạo UI
        self.create_widgets()

    def create_widgets(self):
        # Nút tải ảnh
        self.upload_button = tk.Button(self.master, text="Tải ảnh", command=self.upload_image)
        self.upload_button.pack()

        # Khung hiển thị ảnh gốc
        self.original_image_frame = tk.LabelFrame(self.master, text="Ảnh gốc")
        self.original_image_frame.pack()
        self.original_image_label = tk.Label(self.original_image_frame)
        self.original_image_label.pack()

        # Khung hiển thị ảnh đã tách biên
        self.edged_image_frame = tk.LabelFrame(self.master, text="Ảnh đã tách biên")
        self.edged_image_frame.pack()
        self.edged_image_label = tk.Label(self.edged_image_frame)
        self.edged_image_label.pack()

        # Nút áp dụng tách biên
        self.apply_button = tk.Button(self.master, text="Tách biên", command=self.apply_edge_detection)
        self.apply_button.pack()

    def upload_image(self):
        # Mở hộp thoại chọn file
        file_path = filedialog.askopenfilename()
        if file_path:
            # Mở ảnh và hiển thị
            self.original_image = Image.open(file_path).convert("L")  # Chuyển sang ảnh xám
            self.show_image(self.original_image, self.original_image_label)

    def show_image(self, image, label):
        # Hiển thị ảnh trên label
        photo = ImageTk.PhotoImage(image)
        label.config(image=photo)
        label.image = photo

    def apply_edge_detection(self):
        if self.original_image is not None:
            # Chuyển đổi ảnh sang mảng numpy
            image_array = np.array(self.original_image)

            # Áp dụng bộ lọc tách biên (ví dụ: Laplacian)
            edged_image_array = ndimage.laplace(image_array)

            # Chuyển đổi kết quả thành ảnh
            self.edged_image = Image.fromarray(np.uint8(np.abs(edged_image_array)))

            # Hiển thị ảnh đã tách biên
            self.show_image(self.edged_image, self.edged_image_label)

root = tk.Tk()
app = EdgeDetectionApp(root)
root.mainloop()