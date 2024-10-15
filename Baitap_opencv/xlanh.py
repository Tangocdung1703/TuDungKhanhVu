import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk


# Hàm chọn ảnh từ máy tính
def open_image():
    global panelA, panelB, image, processed_image
    path = filedialog.askopenfilename()

    if len(path) > 0:
        # Đọc ảnh gốc và hiển thị lên giao diện
        image = cv2.imread(path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_tk = ImageTk.PhotoImage(image_pil)

        if panelA is None:
            panelA = Label(image=image_tk)
            panelA.image = image_tk
            panelA.pack(side="left", padx=10, pady=10)
        else:
            panelA.configure(image=image_tk)
            panelA.image = image_tk

        # Thực hiện xử lý ảnh và hiển thị kết quả
        processed_image = process_image(image)
        processed_image_rgb = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
        processed_image_pil = Image.fromarray(processed_image_rgb)
        processed_image_tk = ImageTk.PhotoImage(processed_image_pil)

        if panelB is None:
            panelB = Label(image=processed_image_tk)
            panelB.image = processed_image_tk
            panelB.pack(side="right", padx=10, pady=10)
        else:
            panelB.configure(image=processed_image_tk)
            panelB.image = processed_image_tk


# Hàm xử lý ảnh (tách vật thể và làm mờ phông)
def process_image(image):
    # Khởi tạo mask cho GrabCut
    mask = np.zeros(image.shape[:2], np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    # Chọn vùng bao quanh đối tượng
    rect = (50, 50, image.shape[1] - 50, image.shape[0] - 50)

    # Áp dụng thuật toán GrabCut
    cv2.grabCut(image, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

    # Tạo mask cho đối tượng
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

    # Làm mờ phông nền
    blurred_background = cv2.GaussianBlur(image, (21, 21), 0)

    # Phối lại ảnh sau khi tách đối tượng với phông nền mờ
    final_image = blurred_background.copy()
    final_image[mask2 == 1] = image[mask2 == 1]

    return final_image


# Tạo giao diện người dùng bằng Tkinter
root = Tk()
panelA = None
panelB = None

btn = Button(root, text="Chọn ảnh", command=open_image)
btn.pack(side="top", fill="both", expand="yes", padx=10, pady=10)

root.mainloop()
