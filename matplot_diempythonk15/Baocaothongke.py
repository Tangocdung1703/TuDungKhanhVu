import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Đọc dữ liệu từ file CSV
df = pd.read_csv('diemPython.csv', header=0)

# Chuyển đổi DataFrame thành mảng numpy
in_data = df.to_numpy()

# Trích xuất các cột dữ liệu cần thiết
tongsv = in_data[:, 2]  # Cột thứ 3: Tổng số sinh viên (index 2)
tongsvabc = in_data[:, [4, 5, 6]]  # Các cột điểm A, B+, B (index 4, 5, 6)
tongsvlonhonD = in_data[:, 4:11]  # Các cột điểm từ A đến D+ (index 4 đến 10)
sinhvienlonhondmoilop = in_data[:, 11]  # Cột 12: số lượng sinh viên có điểm >= D (index 11)

# Tính tổng số lượng sinh viên theo từng nhóm
total_students = np.sum(tongsv)
total_ABC = np.sum(tongsvabc)
total_londonD = np.sum(tongsvlonhonD)
total_sinhvienlonhonD = np.sum(sinhvienlonhondmoilop)

# Hiển thị báo cáo tổng số lượng sinh viên
print("---- Báo cáo thống kê điểm học phần Python của sinh viên ----")
print(f"Tổng số sinh viên: {total_students}")
print(f"Tổng số sinh viên đạt A, B+, B: {total_ABC}")
print(f"Tổng số sinh viên có điểm >= D: {total_londonD}")

# Vẽ biểu đồ tổng số sinh viên
plt.figure(figsize=(8, 6))
plt.bar(["Tổng số sinh viên"], [total_students], color='skyblue', label='Tổng số SV')
plt.bar(["Tổng A, B+, B"], [total_ABC], color='orange', label='Tổng ABC')
plt.bar(["Tổng >=D"], [total_londonD], color='green', label='Tổng >=D')
plt.ylabel("Số lượng sinh viên")
plt.title("Tổng số lượng sinh viên theo các tiêu chí")
plt.legend()
plt.show()

# Vẽ biểu đồ số lượng sinh viên đạt điểm >= D cho từng lớp
data_lop = pd.DataFrame({
    'Lớp': df['Mã lớp'],
    'Tổng sinh viên đạt điểm >= D': sinhvienlonhondmoilop
})

plt.figure(figsize=(12, 6))
plt.bar(data_lop['Lớp'], data_lop['Tổng sinh viên đạt điểm >= D'], color='purple')
plt.xlabel("Lớp")
plt.ylabel("Tổng số sinh viên đạt điểm >= D")
plt.title("Tổng số sinh viên đạt điểm >= D theo từng lớp")
plt.xticks(rotation=45)
plt.show()

# Xác định lớp có số lượng điểm A nhiều nhất
a_counts = in_data[:, 4]  # Cột thứ 5 là điểm A (index 4)
max_a = np.argmax(a_counts)  # Tìm chỉ số của lớp có số lượng sinh viên đạt điểm A nhiều nhất
class_with_most_a = df.iloc[max_a, 1]  # Lấy tên lớp tương ứng (index 1 là cột "Mã lớp")
max_a_count = a_counts[max_a]  # Số lượng điểm A của lớp này

print(f'Lớp có số lượng sinh viên đạt điểm A nhiều nhất là: {class_with_most_a} với {max_a_count} điểm A')

# Vẽ biểu đồ phân bố số lượng điểm A của từng lớp
plt.figure(figsize=(12, 6))
plt.bar(df['Mã lớp'], a_counts, color='cyan')
plt.xlabel("Lớp")
plt.ylabel("Số lượng sinh viên đạt điểm A")
plt.title("Phân bố số lượng sinh viên đạt điểm A theo từng lớp")
plt.xticks(rotation=45)
plt.show()

# Vẽ biểu đồ phân bố điểm A, B+ (Histogram)
plt.figure(figsize=(12, 6))
plt.hist(in_data[:, 4], bins=10, alpha=0.5, label='Điểm A', color='red')
plt.hist(in_data[:, 5], bins=10, alpha=0.5, label='Điểm B+', color='blue')
plt.xlabel("Số lượng sinh viên")
plt.ylabel("Tần suất")
plt.title("Phân bố điểm A và B+ của sinh viên")
plt.legend()
plt.show()

# Vẽ biểu đồ tổng hợp số lượng sinh viên đạt từng loại điểm
categories = ["A", "B+", "B", "C+", "C", "D+", "D", "F"]
category_counts = [np.sum(in_data[:, i]) for i in range(4, 12)]  # Tính tổng số lượng từng loại điểm

plt.figure(figsize=(10, 6))
plt.bar(categories, category_counts, color='orange')
plt.xlabel("Loại điểm")
plt.ylabel("Số lượng sinh viên")
plt.title("Phân bố số lượng sinh viên theo từng loại điểm")
plt.show()
