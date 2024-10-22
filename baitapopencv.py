import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

def load_images():
    # Chọn nhiều file hình ảnh
    file_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if not file_paths:
        return

    # Đọc các hình ảnh
    global images, filtered_images
    images = [cv2.imread(file_path) for file_path in file_paths]
    filtered_images = images.copy()  # Khởi tạo danh sách để lưu ảnh đã lọc

    if any(img is None for img in images):
        messagebox.showerror("Error", "Không thể mở hoặc đọc file hình ảnh.")
    else:
        messagebox.showinfo("Thông báo", f"{len(images)} hình ảnh đã được tải thành công.")

def display_image(image, title):
    # Hiển thị hình ảnh bằng OpenCV với tiêu đề đơn giản
    cv2.imshow(title, image)

def apply_sharpen_filter():
    if not images:
        messagebox.showerror("Error", "Chưa chọn hình ảnh.")
        return

    # Khai báo các kernel sharpen
    kernel_sharpen_1 = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    kernel_sharpen_2 = np.array([[1, 1, 1], [1, -7, 1], [1, 1, 1]])
    kernel_sharpen_3 = np.array([[-1, -1, -1, -1, -1],
                                 [-1, 2, 2, 2, -1],
                                 [-1, 2, 8, 2, -1],
                                 [-1, 2, 2, 2, -1],
                                 [-1, -1, -1, -1, -1]]) / 8.0

    # Lấy bộ lọc được chọn từ dropdown
    selected_filter = filter_combobox.get()

    global filtered_images  # Sử dụng biến toàn cục để lưu ảnh đã lọc
    for idx, img in enumerate(images):
        if selected_filter == "Original":
            filtered_img = img
        elif selected_filter == "Sharpening":
            filtered_img = cv2.filter2D(img, -1, kernel_sharpen_1)
        elif selected_filter == "Excessive Sharpening":
            filtered_img = cv2.filter2D(img, -1, kernel_sharpen_2)
        elif selected_filter == "Edge Enhancement":
            filtered_img = cv2.filter2D(img, -1, kernel_sharpen_3)
        elif selected_filter == "Black & White":
            filtered_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        elif selected_filter == "Edge Detection":
            filtered_img = cv2.Canny(img, 100, 200)
        elif selected_filter == "Background Removal":
            filtered_img = remove_background(img)  # Gọi hàm xóa phông

        filtered_images[idx] = filtered_img  # Cập nhật ảnh đã lọc vào danh sách

        # Hiển thị hình ảnh đã áp dụng bộ lọc
        display_image(filtered_img, f"Filtered Image {idx + 1}: {selected_filter}")

def remove_background(img):
    # Sử dụng GrabCut để xóa phông và giữ lại người
    mask = np.zeros(img.shape[:2], np.uint8)

    # Khởi tạo các mảng background và foreground
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    # Tạo một hình chữ nhật bao quanh đối tượng chính (người)
    height, width = img.shape[:2]
    rect = (10, 10, width - 10, height - 10)

    # Áp dụng GrabCut
    cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

    # Tạo mặt nạ cuối cùng để giữ lại phần đối tượng chính
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

    # Áp dụng mặt nạ lên ảnh gốc để xóa phông
    img_foreground = img * mask2[:, :, np.newaxis]

    return img_foreground

def save_images():
    if not filtered_images:
        messagebox.showerror("Error", "Chưa có hình ảnh để lưu.")
        return

    save_dir = filedialog.askdirectory()
    if not save_dir:
        return

    # Lưu từng ảnh đã lọc vào thư mục đã chọn
    for idx, img in enumerate(filtered_images):
        file_name = f"{save_dir}/filtered_image_{idx + 1}.jpg"
        cv2.imwrite(file_name, img)  # Lưu ảnh đã được lọc
    messagebox.showinfo("Thông báo", f"Hình ảnh đã được lưu thành công tại {save_dir}")

# Khởi tạo cửa sổ Tkinter
root = tk.Tk()
root.title("Chọn Bộ Lọc Sắc Nét")

# Khai báo biến hình ảnh
images = []
filtered_images = []

# Nút tải hình ảnh
load_button = tk.Button(root, text="Tải Hình Ảnh", command=load_images)
load_button.pack(pady=10)

# Dropdown để chọn bộ lọc
filter_label = tk.Label(root, text="Chọn bộ lọc:")
filter_label.pack(pady=5)

filters = ["Original", "Sharpening", "Excessive Sharpening", "Edge Enhancement", "Black & White", "Edge Detection", "Background Removal"]
filter_combobox = ttk.Combobox(root, values=filters)
filter_combobox.set("Original")
filter_combobox.pack(pady=5)

# Nút áp dụng bộ lọc
apply_button = tk.Button(root, text="Áp Dụng Bộ Lọc", command=apply_sharpen_filter)
apply_button.pack(pady=10)

# Nút lưu hình ảnh
save_button = tk.Button(root, text="Lưu Hình Ảnh", command=save_images)
save_button.pack(pady=10)

# Chạy vòng lặp chính của Tkinter
root.mainloop()
