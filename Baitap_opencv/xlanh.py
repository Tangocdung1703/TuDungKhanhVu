import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np

def chon_anh():
    global img_goc, roi_selected
    filepath = filedialog.askopenfilename(
        initialdir="/",
        title="Chọn ảnh",
        filetypes=(("Image files", "*.jpg *.jpeg *.png"), ("All files", "*.*"))
    )
    if filepath:
        img_goc = cv2.imread(filepath)
        hien_thi_anh(img_goc, anh_goc_label)

        # Reset ROI khi chọn ảnh mới
        roi_selected = False

def hien_thi_anh(img_cv2, label):
    img_rgb = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)
    label.config(image=img_tk)
    label.image = img_tk

def xoa_phong():
    global img_goc, mask, rect
    if img_goc is not None and roi_selected:
        # Thực hiện GrabCut
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)
        cv2.grabCut(img_goc, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_MASK)

        # Tạo mặt nạ cuối cùng (0 và 2 là nền, 1 và 3 là tiền cảnh)
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

        # Áp dụng mặt nạ lên ảnh gốc
        img_xoa_phong = img_goc * mask2[:, :, np.newaxis]
        hien_thi_anh(img_xoa_phong, anh_ket_qua_label)

def ve_hinh_chu_nhat(event, x, y, flags, param):
    global rect, start_point, end_point, drawing, roi_selected, mask
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_point = (x, y)
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            end_point = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        end_point = (x, y)
        rect = (min(start_point[0], end_point[0]),
                min(start_point[1], end_point[1]),
                abs(end_point[0] - start_point[0]),
                abs(end_point[1] - start_point[1]))
        roi_selected = True
        # Tạo mask ban đầu dựa trên hình chữ nhật
        mask = np.zeros(img_goc.shape[:2], np.uint8)
        mask[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]] = 1

# Tạo cửa sổ giao diện
window = tk.Tk()
window.title("Xóa phông ảnh")

img_goc = None
mask = None
rect = (0, 0, 0, 0)
start_point = (0, 0)
end_point = (0, 0)
drawing = False
roi_selected = False

# Nút chọn ảnh
chon_anh_btn = tk.Button(window, text="Chọn ảnh", command=chon_anh)
chon_anh_btn.pack(pady=10)

# Khung chứa ảnh gốc
anh_goc_label = tk.Label(window)
anh_goc_label.pack(side="left", padx=10)

# Khung chứa ảnh đã xử lý
anh_ket_qua_label = tk.Label(window)
anh_ket_qua_label.pack(side="right", padx=10)

# Nút xóa phông
xoa_phong_btn = tk.Button(window, text="Xóa phông", command=xoa_phong)
xoa_phong_btn.pack(pady=10)

# Lắng nghe sự kiện chuột trên ảnh gốc
cv2.namedWindow("Anh goc")
cv2.setMouseCallback("Anh goc", ve_hinh_chu_nhat)

window.mainloop()