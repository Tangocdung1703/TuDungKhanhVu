import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import neighbors
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler

def chon_tep():
    global df
    duong_dan_tep = filedialog.askopenfilename(filetypes=[("Tệp CSV", "*.csv")])
    if duong_dan_tep:
        try:
            df = pd.read_csv(duong_dan_tep)
            nhan_tep.config(text=duong_dan_tep)
            nut_huan_luyen.config(state="normal")
        except Exception as e:
            print(f"Lỗi đọc tệp: {e}")
            nhan_tep.config(text="Lỗi đọc tệp")


def huan_luyen_mo_hinh():
    global X_train, X_test, y_train, y_test, model, y_predict
    try:
        X = np.array(df.iloc[:, :-1]).astype(np.float64)
        y = np.array(df.iloc[:, -1:]).astype(np.float64)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
        y_train = y_train.ravel()
        y_test = y_test.ravel()

        thuat_toan = bien_thuat_toan.get()

        if thuat_toan == "KNN":
            model = neighbors.KNeighborsRegressor(n_neighbors=3, p=2)
        elif thuat_toan == "Hồi quy tuyến tính":
            model = LinearRegression()
        elif thuat_toan == "DTR":
            model = DecisionTreeRegressor()
        elif thuat_toan == "SVR":
            
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            model = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=.1)
            model.fit(X_train_scaled, y_train)  # Huấn luyện trên dữ liệu đã được scale
            y_predict = model.predict(X_test_scaled)  # Dự đoán trên dữ liệu đã được scale

        # Loại bỏ dòng model.fit(X_train, y_train) ở đây vì nó ghi đè lên mô hình SVR

        # Nếu không phải SVR, huấn luyện mô hình ở đây:
        if thuat_toan != "SVR":
            model.fit(X_train, y_train)
            y_predict = model.predict(X_test)

        mse = mean_squared_error(y_test, y_predict)
        mae = mean_absolute_error(y_test, y_predict)
        rmse = np.sqrt(mse)

        nhan_mse.config(text=f"MSE: {mse:.2f}")
        nhan_mae.config(text=f"MAE: {mae:.2f}")
        nhan_rmse.config(text=f"RMSE: {rmse:.2f}")

        so_luong_loi = {
            "<1": np.sum(abs(y_test - y_predict) < 1),
            "1-2": np.sum((abs(y_test - y_predict) >= 1) & (abs(y_test - y_predict) < 2)),
            ">2": np.sum(abs(y_test - y_predict) >= 2)
        }

        plt.figure(figsize=(10, 5))

        plt.subplot(1, 2, 1)
        plt.plot(range(len(y_test)), y_test, 'ro', label='Dữ liệu gốc')
        plt.plot(range(len(y_predict)), y_predict, 'bo', label='Dữ liệu dự đoán')
        for i in range(len(y_test)):
            plt.plot([i, i], [y_test[i], y_predict[i]], 'g')
        plt.title('Thực tế vs. Dự đoán')
        plt.legend()

        plt.subplot(1, 2, 2)
        nhan = so_luong_loi.keys()
        kich_thuoc = so_luong_loi.values()
        plt.bar(nhan, kich_thuoc)
        plt.title('Phân bố lỗi')
        plt.show()

        nut_du_doan.config(state="normal")

    except Exception as e:
        print(f"Lỗi trong quá trình huấn luyện: {e}")
        nhan_mse.config(text="Lỗi huấn luyện")

def huan_luyen_va_ve_do_thi():
    # Xóa biểu đồ cũ nếu có
    for widget in root.winfo_children():
        if isinstance(widget, FigureCanvasTkAgg):
            widget.destroy()
    global X_train, X_test, y_train, y_test, df, scaler

    try:
        X = np.array(df.iloc[:, :-1]).astype(np.float64)
        y = np.array(df.iloc[:, -1:]).astype(np.float64).ravel()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

        models = {
            "KNN": KNeighborsRegressor(n_neighbors=3, p=2),
            "Hồi quy tuyến tính": LinearRegression(),
            "DTR": DecisionTreeRegressor(),
            "SVR": SVR(kernel='rbf', C=100, gamma=0.1, epsilon=.1),
        }

        bieu_do_dang = bien_bieu_do.get()

        if bieu_do_dang == "cot":
            fig, ax = plt.subplots(figsize=(12, 6))
            mse_values = []
            model_names = list(models.keys())

            for name, model in models.items():
                if name == "SVR":
                    scaler = StandardScaler()
                    X_train_scaled = scaler.fit_transform(X_train)
                    X_test_scaled = scaler.transform(X_test)
                    model.fit(X_train_scaled, y_train)
                    y_predict = model.predict(X_test_scaled)
                else:
                    model.fit(X_train, y_train)
                    y_predict = model.predict(X_test)

                mse = mean_squared_error(y_test, y_predict)
                mse_values.append(mse)

            ax.bar(model_names, mse_values)
            ax.set_ylabel('MSE')
            ax.set_title('So sánh MSE của các mô hình')


        elif bieu_do_dang == "duong":
            fig, ax = plt.subplots(figsize=(12, 6))

            for name, model in models.items():
                if name == "SVR":
                    scaler = StandardScaler()
                    X_train_scaled = scaler.fit_transform(X_train)
                    X_test_scaled = scaler.transform(X_test)
                    model.fit(X_train_scaled, y_train)
                    y_predict = model.predict(X_test_scaled)
                else:
                    model.fit(X_train, y_train)
                    y_predict = model.predict(X_test)

                mse = mean_squared_error(y_test, y_predict)
                ax.plot(range(len(y_test)), y_predict, label=f'{name} (MSE: {mse:.2f})')

            ax.plot(range(len(y_test)), y_test, 'ro', label='Dữ liệu gốc')
            ax.set_title('So sánh các mô hình')
            ax.legend()

        else:
            print("Loại biểu đồ không hợp lệ.")
            return

        # Xóa biểu đồ cũ nếu có
        for widget in root.winfo_children():
            if isinstance(widget, FigureCanvasTkAgg):
                widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack()

    except Exception as fe:
        print(f"Lỗi trong quá trình huấn luyện: {e}")

scaler = StandardScaler()

# def du_doan_du_lieu_moi():
#     try:
#         gio_hoc = float(nhap_gio_hoc.get())
#         diem_truoc = float(nhap_diem_truoc.get())
#         hoat_dong_ngoai_khoa = float(nhap_hoat_dong_ngoai_khoa.get())
#         gio_ngu = float(nhap_gio_ngu.get())
#         so_bai_tap = float(nhap_so_bai_tap.get())

#         du_lieu_moi = np.array([gio_hoc, diem_truoc, hoat_dong_ngoai_khoa, gio_ngu, so_bai_tap]).reshape(1, -1)

#         thuat_toan = bien_thuat_toan.get()

#         if thuat_toan == "KNN":
#             model = KNeighborsRegressor(n_neighbors=3, p=2)
#         elif thuat_toan == "Hồi quy tuyến tính":
#             model = LinearRegression()
#         elif thuat_toan == "DTR":
#             model = DecisionTreeRegressor()
#         elif thuat_toan == "SVR":
#             model = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=.1)
#             du_lieu_moi = scaler.transform(du_lieu_moi) # Scale dữ liệu cho SVR
#             X_train_scaled = scaler.transform(X_train) # Scale X_train cho SVR
#         else:
#             raise ValueError("Thuật toán không hợp lệ.")

#         # Fit và dự đoán (chỉ một lần)
#         model.fit(X_train_scaled if thuat_toan == "SVR" else X_train, y_train)
#         du_doan = model.predict(du_lieu_moi)
#         nhan_du_doan.config(text=f"Dự đoán: {du_doan[0]:.2f}")

#     except ValueError:
#         nhan_du_doan.config(text="Định dạng đầu vào không hợp lệ. Vui lòng nhập số.")
#     except Exception as e:
#         print(f"Lỗi dự đoán: {e}")
#         nhan_du_doan.config(text="Lỗi dự đoán")

from sklearn.preprocessing import StandardScaler


def du_doan_du_lieu_moi():
    try:
        X = np.array(df.iloc[:, :-1]).astype(np.float64)
        y = np.array(df.iloc[:, -1:]).astype(np.float64).ravel()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
        # Khởi tạo scaler *bên ngoài* hàm
        scaler = StandardScaler()

        # Fit scaler với dữ liệu huấn luyện *một lần* trước khi gọi hàm dự đoán
        X_train_scaled = scaler.fit_transform(X_train)
        gio_hoc = float(nhap_gio_hoc.get())
        diem_truoc = float(nhap_diem_truoc.get())
        hoat_dong_ngoai_khoa = float(nhap_hoat_dong_ngoai_khoa.get())
        gio_ngu = float(nhap_gio_ngu.get())
        so_bai_tap = float(nhap_so_bai_tap.get())

        du_lieu_moi = np.array([gio_hoc, diem_truoc, hoat_dong_ngoai_khoa, gio_ngu, so_bai_tap]).reshape(1, -1)

        thuat_toan = bien_thuat_toan.get()

        # Khởi tạo mô hình và huấn luyện *bên ngoài* hàm, chỉ một lần
        if thuat_toan == "KNN":
            model = KNeighborsRegressor(n_neighbors=3, p=2)
        elif thuat_toan == "Hồi quy tuyến tính":
            model = LinearRegression()
        elif thuat_toan == "DTR":
            model = DecisionTreeRegressor()
        elif thuat_toan == "SVR":
            model = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=.1)
        else:
            raise ValueError("Thuật toán không hợp lệ.")

        model.fit(X_train_scaled if thuat_toan == "SVR" else X_train, y_train)

        # Scale dữ liệu mới nếu sử dụng SVR
        if thuat_toan == "SVR":
            du_lieu_moi = scaler.transform(du_lieu_moi)

        du_doan = model.predict(du_lieu_moi)
        nhan_du_doan.config(text=f"Dự đoán: {du_doan[0]:.2f}")

    except ValueError:
        nhan_du_doan.config(text="Định dạng đầu vào không hợp lệ. Vui lòng nhập số.")
    except Exception as e:
        print(f"Lỗi dự đoán: {e}")
        nhan_du_doan.config(text="Lỗi dự đoán")

root = tk.Tk()
root.title("Dự đoán Điểm Sinh Viên")


nhan_tep = tk.Label(root, text="Chưa chọn tệp")
nhan_tep.pack()

nut_chon_tep = tk.Button(root, text="Chọn tệp CSV", command=chon_tep)
nut_chon_tep.pack()


bien_thuat_toan = tk.StringVar(value="KNN")

khung_thuat_toan = tk.LabelFrame(root, text="Chọn thuật toán") #Thêm khung cho thuật toán
khung_thuat_toan.pack()

# Sử dụng radiobuttons trong khung
nut_chon_knn = tk.Radiobutton(khung_thuat_toan, text="KNN", variable=bien_thuat_toan, value="KNN")
nut_chon_knn.pack(side=tk.LEFT)

nut_chon_hoi_quy_tuyen_tinh = tk.Radiobutton(khung_thuat_toan, text="Hồi quy tuyến tính", variable=bien_thuat_toan, value="Hồi quy tuyến tính")
nut_chon_hoi_quy_tuyen_tinh.pack(side=tk.LEFT)

nut_chon_dtr = tk.Radiobutton(khung_thuat_toan, text="DTR", variable=bien_thuat_toan, value="DTR")
nut_chon_dtr.pack(side=tk.LEFT)

nut_chon_svr = tk.Radiobutton(khung_thuat_toan, text="SVR", variable=bien_thuat_toan, value="SVR")
nut_chon_svr.pack(side=tk.LEFT)


nut_huan_luyen = tk.Button(root, text="Huấn luyện mô hình", command=huan_luyen_mo_hinh, state="disabled")
nut_huan_luyen.pack()


nut_so_sanh = tk.Button(root, text="So sánh mô hình", command=huan_luyen_va_ve_do_thi) # Bắt đầu ở trạng thái disabled
nut_so_sanh.pack()

bien_bieu_do = tk.StringVar(value="duong")  # Biến lưu loại biểu đồ

khung_bieu_do = tk.LabelFrame(root, text="Chọn dạng biểu đồ")
khung_bieu_do.pack()

nut_chon_cot = tk.Radiobutton(khung_bieu_do, text="Cột", variable=bien_bieu_do, value="cot")
nut_chon_cot.pack(side=tk.LEFT)

# nut_chon_duong = tk.Radiobutton(khung_bieu_do, text="Đường", variable=bien_bieu_do, value="duong")
# nut_chon_duong.pack(side=tk.LEFT)

nhan_mse = tk.Label(root, text="")
nhan_mse.pack()

nhan_mae = tk.Label(root, text="")
nhan_mae.pack()

nhan_rmse = tk.Label(root, text="")
nhan_rmse.pack()


khung_nhap_du_lieu = tk.LabelFrame(root, text="Nhập dữ liệu mới")
khung_nhap_du_lieu.pack(pady=10)

nhan_gio_hoc = tk.Label(khung_nhap_du_lieu, text="Giờ học:")
nhan_gio_hoc.grid(row=0, column=0)
nhap_gio_hoc = tk.Entry(khung_nhap_du_lieu)
nhap_gio_hoc.grid(row=0, column=1)

nhan_diem_truoc = tk.Label(khung_nhap_du_lieu, text="Điểm trước:")
nhan_diem_truoc.grid(row=1, column=0)
nhap_diem_truoc = tk.Entry(khung_nhap_du_lieu)
nhap_diem_truoc.grid(row=1, column=1)


nhan_hoat_dong_ngoai_khoa = tk.Label(khung_nhap_du_lieu, text="Hoạt động ngoại khóa (1 cho Có, 0 cho Không):")
nhan_hoat_dong_ngoai_khoa.grid(row=2, column=0)
nhap_hoat_dong_ngoai_khoa = tk.Entry(khung_nhap_du_lieu)
nhap_hoat_dong_ngoai_khoa.grid(row=2, column=1)

nhan_gio_ngu = tk.Label(khung_nhap_du_lieu, text="Giờ ngủ:")
nhan_gio_ngu.grid(row=3, column=0)
nhap_gio_ngu = tk.Entry(khung_nhap_du_lieu)
nhap_gio_ngu.grid(row=3, column=1)

nhan_so_bai_tap = tk.Label(khung_nhap_du_lieu, text="Số bài tập đã làm:")
nhan_so_bai_tap.grid(row=4, column=0)
nhap_so_bai_tap = tk.Entry(khung_nhap_du_lieu)
nhap_so_bai_tap.grid(row=4, column=1)


nut_du_doan = tk.Button(root, text="Dự đoán", command=du_doan_du_lieu_moi, state="disabled")
nut_du_doan.pack()

nhan_du_doan = tk.Label(root, text="")
nhan_du_doan.pack()

root.mainloop()