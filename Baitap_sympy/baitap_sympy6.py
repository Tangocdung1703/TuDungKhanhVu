print("Ứng dụng tạo bộ lọc ảnh số")
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sympy.discrete.transforms import fft, ifft

class ImageFilterApp:
    def __init__(self, master):
        self.master = master
        master.title("Bộ lọc ảnh số")

        # Khởi tạo biến
        self.original_image = None
        self.filtered_image = None
        self.filter_type = tk.StringVar(value="Low-pass")  # Mặc định là Low-pass filter

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

        # Khung hiển thị ảnh đã lọc
        self.filtered_image_frame = tk.LabelFrame(self.master, text="Ảnh đã lọc")
        self.filtered_image_frame.pack()
        self.filtered_image_label = tk.Label(self.filtered_image_frame)
        self.filtered_image_label.pack()

        # Chọn loại bộ lọc
        self.filter_label = tk.Label(self.master, text="Chọn loại bộ lọc:")
        self.filter_label.pack()

        self.filter_options = ["Low-pass", "High-pass"]
        self.filter_dropdown = tk.OptionMenu(self.master, self.filter_type, *self.filter_options)
        self.filter_dropdown.pack()

        # Nút áp dụng bộ lọc
        self.apply_button = tk.Button(self.master, text="Áp dụng bộ lọc", command=self.apply_filter)
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

    def apply_filter(self):
        if self.original_image is not None:
            # Chuyển đổi ảnh sang mảng numpy
            image_array = np.array(self.original_image)

            # Áp dụng FFT
            fft_image = fft(image_array)

            # Tạo bộ lọc dựa trên lựa chọn
            if self.filter_type.get() == "Low-pass":
                filtered_fft = self.apply_low_pass_filter(fft_image)
            elif self.filter_type.get() == "High-pass":
                filtered_fft = self.apply_high_pass_filter(fft_image)
            else:
                print("Lựa chọn bộ lọc không hợp lệ.")
                return

            # Áp dụng IFFT để chuyển đổi ngược lại thành ảnh
            self.filtered_image = Image.fromarray(np.uint8(ifft(filtered_fft).real))

            # Hiển thị ảnh đã lọc
            self.show_image(self.filtered_image, self.filtered_image_label)

    def apply_low_pass_filter(self, fft_image):
        # Áp dụng bộ lọc low-pass (ví dụ: Gaussian filter)
        # ... (Thêm logic của bạn tại đây) ...
        return fft_image  # Thay thế bằng kết quả sau khi lọc

    def apply_high_pass_filter(self, fft_image):
        # Áp dụng bộ lọc high-pass
        # ... (Thêm logic của bạn tại đây) ...
        return fft_image  # Thay thế bằng kết quả sau khi lọc

root = tk.Tk()
app = ImageFilterApp(root)
root.mainloop()