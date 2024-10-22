import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np

class ImageFilterApp:
    def __init__(self, master):
        self.master = master
        master.title("Bộ Lọc Ảnh")

        # Biến lưu trữ ảnh
        self.original_image = None
        self.filtered_image = None

        # Tạo giao diện
        self.create_widgets()

    def create_widgets(self):
        # Khung chọn ảnh
        self.image_frame = tk.LabelFrame(self.master, text="Ảnh", padx=10, pady=10)
        self.image_frame.grid(row=0, column=0, padx=10, pady=10)

        # Nút chọn ảnh
        self.upload_button = tk.Button(self.image_frame, text="Chọn Ảnh", command=self.upload_image)
        self.upload_button.pack(pady=5)

        # Hiển thị ảnh
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack()

        # Khung chọn bộ lọc
        self.filter_frame = tk.LabelFrame(self.master, text="Bộ Lọc", padx=10, pady=10)
        self.filter_frame.grid(row=0, column=1, padx=10, pady=10)

        # Nút chọn bộ lọc
        self.filter_options = [
            ("Identity", self.apply_identity_filter),
            ("3x3 Blur", self.apply_3x3_filter),
            ("5x5 Blur", self.apply_5x5_filter),
        ]
        self.filter_var = tk.StringVar(value="Chọn Bộ Lọc")

        for text, command in self.filter_options:
            tk.Radiobutton(
                self.filter_frame,
                text=text,
                variable=self.filter_var,
                value=text,
                command=command,
            ).pack(anchor=tk.W)

    def upload_image(self):
        # Mở hộp thoại chọn file
        file_path = filedialog.askopenfilename(
            initialdir = "/",
            title = "Chọn Ảnh",
            filetypes = (("Image files", "*.jpg *.jpeg *.png *.bmp"), ("all files", "*.*"))
        )
        if file_path:
            try:
                # Đọc ảnh bằng OpenCV
                self.original_image = cv2.imread(file_path)

                # Chuyển đổi ảnh từ BGR sang RGB để hiển thị bằng Tkinter
                img_rgb = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img_rgb)
                img.thumbnail((300, 300))  # Thay đổi kích thước ảnh cho vừa khung
                img_tk = ImageTk.PhotoImage(img)

                # Hiển thị ảnh lên giao diện
                self.image_label.config(image=img_tk)
                self.image_label.image = img_tk  # Giữ reference để ảnh không bị garbage collected

            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể mở ảnh: {e}")

    def apply_filter(self, kernel_size):
        if self.original_image is not None:
            try:
                if kernel_size == "Identity":
                    kernel = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
                elif kernel_size == "3x3 Blur":
                    kernel = np.ones((3, 3), np.float32) / 9.0
                elif kernel_size == "5x5 Blur":
                    kernel = np.ones((5, 5), np.float32) / 25.0
                else:
                    messagebox.showwarning("Cảnh báo", "Chưa chọn bộ lọc.")
                    return

                self.filtered_image = cv2.filter2D(self.original_image, -1, kernel)

                # Chuyển đổi và hiển thị ảnh đã lọc
                filtered_img_rgb = cv2.cvtColor(self.filtered_image, cv2.COLOR_BGR2RGB)
                filtered_img = Image.fromarray(filtered_img_rgb)
                filtered_img.thumbnail((300, 300))
                filtered_img_tk = ImageTk.PhotoImage(filtered_img)
                self.image_label.config(image=filtered_img_tk)
                self.image_label.image = filtered_img_tk

            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể áp dụng bộ lọc: {e}")

    def apply_identity_filter(self):
        self.apply_filter("Identity")

    def apply_3x3_filter(self):
        self.apply_filter("3x3 Blur")

    def apply_5x5_filter(self):
        self.apply_filter("5x5 Blur")

root = tk.Tk()
root.geometry("500x500")
app = ImageFilterApp(root)
root.mainloop()