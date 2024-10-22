import cv2
import numpy as np
import tkinter as tk
from tkinter import Tk, Button, Label, filedialog, OptionMenu, StringVar, Scale, HORIZONTAL
from PIL import ImageTk, Image
import threading

class ImageEditor:
    def __init__(self, master):
        self.master = master
        master.title("Simple Image Editor")

        self.original_image = None
        self.processed_image = None
        self.camera = None

        self.create_widgets()

    def create_widgets(self):
        # Frame chứa ảnh gốc và xử lý
        image_frame = tk.LabelFrame(self.master, text="Hình ảnh")
        image_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self.original_label = Label(image_frame, text="Gốc")
        self.original_label.grid(row=0, column=0, padx=5, pady=5)

        self.processed_label = Label(image_frame, text="Đã xử lý")
        self.processed_label.grid(row=0, column=1, padx=5, pady=5)

        # Frame chứa các nút chức năng (nằm ngang)
        button_frame = tk.Frame(self.master)  # Không cần LabelFrame cho button_frame
        button_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        self.load_button = Button(button_frame, text="Tải ảnh", command=self.load_image)
        self.load_button.pack(side="left", padx=5)

        # self.capture_button = Button(button_frame, text="Mở Camera", command=self.open_camera_window)
        # self.capture_button.pack(side="left", padx=5)

        # self.save_button = Button(button_frame, text="Lưu ảnh", command=self.save_image)
        # self.save_button.pack(side="left", padx=5)

        # Frame chứa lựa chọn filter và các thành phần liên quan
        filter_frame = tk.Frame(self.master)  # Không cần LabelFrame cho filter_frame
        filter_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        self.filter_options = [
            "Không có", "Làm mờ", "Làm sắc nét", "Đen trắng",
            "Làm mờ nền", "Làm sắc nét nền", "CLAHE", "Làm rõ khối u"
        ]
        self.selected_filter = StringVar(self.master)
        self.selected_filter.set(self.filter_options[0])
        self.filter_menu = OptionMenu(filter_frame, self.selected_filter, *self.filter_options)
        self.filter_menu.pack(side="left", padx=5)

        self.apply_button = Button(filter_frame, text="Áp dụng", command=self.apply_filter)
        self.apply_button.pack(side="left", padx=5)

        # Frame chứa thanh trượt cho CLAHE
        clahe_frame = tk.LabelFrame(filter_frame, text="CLAHE")
        clahe_frame.pack(side="left", padx=5)  # Sắp xếp theo chiều ngang

        self.clahe_clip_limit_label = Label(clahe_frame, text="Clip Limit:")
        self.clahe_clip_limit_label.grid(row=0, column=0, pady=5)
        self.clahe_clip_limit_scale = Scale(clahe_frame, from_=1, to=10, orient=HORIZONTAL)
        self.clahe_clip_limit_scale.set(2)
        self.clahe_clip_limit_scale.grid(row=0, column=1, pady=5)

        # Frame chứa thanh trượt cho ngưỡng khối u
        tumor_frame = tk.LabelFrame(filter_frame, text="Khối u")
        tumor_frame.pack(side="left", padx=5)  # Sắp xếp theo chiều ngang

        self.tumor_threshold_label = Label(tumor_frame, text="Ngưỡng:")
        self.tumor_threshold_label.grid(row=0, column=0, pady=5)
        self.tumor_threshold_scale = Scale(tumor_frame, from_=0, to=255, orient=HORIZONTAL)
        self.tumor_threshold_scale.set(128)
        self.tumor_threshold_scale.grid(row=0, column=1, pady=5)


    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.original_image = cv2.imread(file_path)
            self.show_image(self.original_image, self.original_label)

    def open_camera_window(self):
        threading.Thread(target=self.show_camera_and_capture).start()

    def show_camera_and_capture(self):
        self.camera = cv2.VideoCapture(0)

        while(True):
            ret, frame = self.camera.read()
            cv2.imshow('Camera (Nhấn "c" để chụp, "q" để thoát)', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if cv2.waitKey(1) & 0xFF == ord('c'):
                self.original_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.show_image(self.original_image, self.original_label)
                print("Đã chụp ảnh!")

        self.camera.release()
        cv2.destroyAllWindows()

    def apply_filter(self):
        if self.original_image is not None:
            selected_filter = self.selected_filter.get()
            self.processed_image = self.original_image.copy()

            if selected_filter == "Làm mờ":
                self.processed_image = self.apply_blur(self.processed_image)
            elif selected_filter == "Làm sắc nét":
                self.processed_image = self.apply_sharpen(self.processed_image)
            elif selected_filter == "Đen trắng":
                self.processed_image = self.apply_black_and_white(self.processed_image)
            elif selected_filter == "Làm mờ nền":
                self.processed_image = self.apply_background_blur(self.processed_image)
            elif selected_filter == "Làm sắc nét nền":
                self.processed_image = self.apply_sharpen_background(self.processed_image)
            elif selected_filter == "CLAHE":
                self.processed_image = self.apply_clahe(self.processed_image, self.clahe_clip_limit_scale.get())
            elif selected_filter == "Làm rõ khối u":
                self.processed_image = self.highlight_tumor(self.processed_image, self.tumor_threshold_scale.get())

            self.show_image(self.processed_image, self.processed_label)

    def apply_blur(self, img):
        kernel = np.ones((13, 13), np.float32) / 169.0
        return cv2.filter2D(img, -1, kernel)

    def apply_sharpen(self, img):
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        return cv2.filter2D(img, -1, kernel)

    def apply_black_and_white(self, img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def apply_background_blur(self, img):
        blurred_img = cv2.GaussianBlur(img, (9, 9), 0)
        mask = img > 128
        return np.where(mask, img, blurred_img)

    def apply_sharpen_background(self, img):
        sharpened_img = img.copy()
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        sharpened_img = cv2.filter2D(sharpened_img, -1, kernel)
        mask = img > 128
        return np.where(mask, img, sharpened_img)

    def apply_clahe(self, img, clip_limit):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8,8))
        cl1 = clahe.apply(gray)
        return cv2.cvtColor(cl1, cv2.COLOR_GRAY2BGR)

    def highlight_tumor(self, img, threshold):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, tumor_mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

        # Tạo một bản sao của ảnh gốc để chứa kết quả
        highlighted_tumor = img.copy()

        # Tăng độ sáng cho vùng có khối u
        highlighted_tumor[tumor_mask != 0] = np.clip(highlighted_tumor[tumor_mask != 0] + 50, 0, 255).astype(np.uint8)

        return highlighted_tumor

    def show_image(self, img, label):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (500, 500))
        photo = ImageTk.PhotoImage(image=Image.fromarray(img))
        label.config(image=photo)
        label.image = photo
    

    def save_image(self):
        if self.processed_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg")
            if file_path:
                cv2.imwrite(file_path, self.processed_image)

root = Tk()
image_editor = ImageEditor(root)
root.mainloop()