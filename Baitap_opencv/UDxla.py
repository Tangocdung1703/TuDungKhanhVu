import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk

class ImageProcessor:
    def __init__(self, master):
        self.master = master
        master.title("Ứng dụng Xử lý Ảnh")

        self.image = None
        self.filtered_image = None
        self.cap = None

        # Tạo các button
        self.load_button = tk.Button(master, text="Tải ảnh", command=self.load_image)
        self.load_button.pack(pady=5)

        self.capture_button = tk.Button(master, text="Chụp ảnh", command=self.open_camera)
        self.capture_button.pack(pady=5)

        self.filter_options = [
            "Làm mờ",
            "Làm nét",
            "Ảnh đen trắng",
            "Xóa nhiễu",
            "Tăng cường sáng",
            "Làm mịn ảnh"
        ]
        self.filter_var = tk.StringVar(master)
        self.filter_var.set("Chọn bộ lọc")
        self.filter_menu = tk.OptionMenu(master, self.filter_var, *self.filter_options)
        self.filter_menu.pack(pady=5)

        self.apply_button = tk.Button(master, text="Áp dụng", command=self.apply_filter)
        self.apply_button.pack(pady=5)

        self.save_button = tk.Button(master, text="Lưu ảnh", command=self.save_image, state="disabled")
        self.save_button.pack(pady=5)

        # Tạo khung chứa ảnh
        self.image_frame = tk.Frame(master)
        self.image_frame.pack()

        self.original_label = tk.Label(self.image_frame, text="Ảnh gốc")
        self.original_label.grid(row=0, column=0)

        self.processed_label = tk.Label(self.image_frame, text="Ảnh đã xử lý")
        self.processed_label.grid(row=0, column=1)

        self.original_image_label = tk.Label(self.image_frame)
        self.original_image_label.grid(row=1, column=0)

        self.processed_image_label = tk.Label(self.image_frame)
        self.processed_image_label.grid(row=1, column=1)

    def load_image(self):
        """Mở hộp thoại chọn file và hiển thị ảnh."""
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = cv2.imread(file_path)
            self.show_image(self.image, self.original_image_label)
            self.reset_processed_image()

    def open_camera(self):
        """Mở camera và hiển thị trực tiếp."""
        self.cap = cv2.VideoCapture(0)
        if self.cap.isOpened():
            self.master.bind('<Return>', self.capture_from_camera)
            self.show_camera_feed()
        else:
            print("Không thể mở camera.")

    def show_camera_feed(self):
        """Hiển thị luồng video từ camera."""
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = ImageTk.PhotoImage(img)
            self.original_image_label.config(image=img)
            self.original_image_label.image = img
            self.original_image_label.after(10, self.show_camera_feed)

    def capture_from_camera(self, event=None):
        """Chụp ảnh từ camera khi nhấn Enter."""
        if self.cap is not None and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.image = frame
                self.show_image(self.image, self.original_image_label)
                self.reset_processed_image()
            self.cap.release()
            self.master.unbind('<Return>')

    def apply_filter(self):
        """Áp dụng bộ lọc dựa trên lựa chọn và hiển thị ảnh đã xử lý."""
        if self.image is not None:
            filter_type = self.filter_var.get()
            self.filtered_image = self.apply_filter_to_image(self.image.copy(), filter_type)
            self.show_image(self.filtered_image, self.processed_image_label)
            self.save_button.config(state="normal")

    def apply_filter_to_image(self, img, filter_type):
        """Áp dụng bộ lọc lên ảnh."""
        if filter_type == "Làm mờ":
            return cv2.blur(img, (5, 5))
        elif filter_type == "Làm nét":
            kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
            return cv2.filter2D(img, -1, kernel)
        elif filter_type == "Ảnh đen trắng":
            return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        elif filter_type == "Xóa nhiễu":
            return cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
        elif filter_type == "Tăng cường sáng":
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv)
            v_eq = clahe.apply(v)
            hsv_eq = cv2.merge((h, s, v_eq))
            return cv2.cvtColor(hsv_eq, cv2.COLOR_HSV2BGR)
        elif filter_type == "Làm mịn ảnh":
            kernel = np.ones((5, 5), np.float32) / 25.0
            return cv2.filter2D(img, -1, kernel)
        else:
            return img

    def save_image(self):
        """Lưu ảnh đã xử lý."""
        if self.filtered_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg")
            if file_path:
                cv2.imwrite(file_path, self.filtered_image)

    def show_image(self, img, label):
        """Hiển thị ảnh lên label."""
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        label.config(image=img)
        label.image = img

    def reset_processed_image(self):
        """Reset ảnh đã xử lý."""
        self.processed_image_label.config(image="")
        self.save_button.config(state="disabled")

root = tk.Tk()
app = ImageProcessor(root)
root.mainloop()