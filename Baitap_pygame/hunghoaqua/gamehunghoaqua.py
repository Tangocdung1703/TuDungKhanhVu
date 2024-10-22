import pygame, sys
from pygame.locals import *
import random

chieu_dai = 800  # Chiều dài cửa sổ
chieu_rong = 500  # Chiều cao cửa sổ
pygame.init()  # Khởi tạo game

# Khởi tạo mô-đun âm thanh và nhạc nền
pygame.mixer.init()

w = pygame.display.set_mode((chieu_dai, chieu_rong))  # Tạo cửa sổ game
pygame.display.set_caption('Hứng hoa quả demo nhóm 7')

# Khởi tạo giá trị ban đầu
score = 0
lives = 3
paused = False  # Trạng thái tạm dừng

# Tạo nền của game
anh_nen = pygame.image.load('bg2.jpg')
anh_nen = pygame.transform.scale(anh_nen, (chieu_dai, chieu_rong))

# Tạo các hình ảnh quả
tao = pygame.image.load('tao.png')
tao = pygame.transform.scale(tao, (60, 70))
cam = pygame.image.load('cam.png')
cam = pygame.transform.scale(cam, (60, 70))
xoai = pygame.image.load('xoai.png')
xoai = pygame.transform.scale(xoai, (60, 70))

# Vị trí ban đầu của quả
x_tao, y_tao = 100, 0
x_cam, y_cam = 200, 0
x_xoai, y_xoai = 300, 0

# Giỏ để hứng quả
gio = pygame.image.load('gio.png')
gio = pygame.transform.scale(gio, (120, 100))

# Vị trí của giỏ
x_gio, y_gio = chieu_dai // 2, chieu_rong - 100

# Tốc độ của quả (chọn độ khó)
toc_do_tao, toc_do_cam, toc_do_xoai = 1, 2, 3

# Khởi tạo khung thời gian
FPS = 60
fpsClock = pygame.time.Clock()

# Hàm kiểm tra quả rơi trúng giỏ
def kiem_tra_hung_fruit(x_fruit, y_fruit):
    global score, lives
    if y_fruit >= y_gio and x_gio <= x_fruit <= (x_gio + 120):
        score += 5
        return True
    elif y_fruit > chieu_rong:
        lives -= 1
        return True
    return False

# Hàm lưu điểm số vào file
def ghi_diem():
    with open('diemso.txt', 'a') as file:
        file.write(f'{score}\n')

# Hàm hiển thị bảng xếp hạng
def hien_thi_xep_hang():
    try:
        with open('diemso.txt', 'r') as file:
            diem = [int(d) for d in file.readlines()]
        diem.sort(reverse=True)
        return diem[:5]  # Lấy top 5
    except FileNotFoundError:
        return []

# Màn hình chọn độ khó
def chon_do_kho():
    global toc_do_tao, toc_do_cam, toc_do_xoai
    chon_kho = True
    while chon_kho:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_1:  # Dễ
                    toc_do_tao, toc_do_cam, toc_do_xoai = 1, 2, 3
                    chon_kho = False
                elif event.key == K_2:  # Trung bình
                    toc_do_tao, toc_do_cam, toc_do_xoai = 3, 5, 7
                    chon_kho = False
                elif event.key == K_3:  # Khó
                    toc_do_tao, toc_do_cam, toc_do_xoai = 5, 7, 9
                    chon_kho = False

        font = pygame.font.SysFont(None, 48)
        w.fill((0, 0, 0))
        text = font.render(f"level: 1 - easy, 2 - normal, 3 - hard", True, (255, 255, 255))
        w.blit(text, (chieu_dai//10, chieu_rong//2))
        pygame.display.update()

chon_do_kho()

# Vòng lặp game chính
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_p:
                paused = not paused  # Chức năng tạm dừng

    if not paused:
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and x_gio > 0:
            x_gio -= 5
        if keys[K_RIGHT] and x_gio < chieu_dai - 120:
            x_gio += 5

        if lives <= 0:
            print("Game Over! Your final score is:", score)
            ghi_diem()
            print("Bảng xếp hạng:", hien_thi_xep_hang())
            pygame.quit()
            sys.exit()

        w.blit(anh_nen, (0, 0))
        w.blit(gio, (x_gio, y_gio))

        w.blit(tao, (x_tao, y_tao))
        w.blit(cam, (x_cam, y_cam))
        w.blit(xoai, (x_xoai, y_xoai))

        y_tao += toc_do_tao
        y_cam += toc_do_cam
        y_xoai += toc_do_xoai

        if kiem_tra_hung_fruit(x_tao, y_tao):
            y_tao = 0
            x_tao = random.randint(0, chieu_dai - 60)
        if kiem_tra_hung_fruit(x_cam, y_cam):
            y_cam = 0
            x_cam = random.randint(0, chieu_dai - 60)
        if kiem_tra_hung_fruit(x_xoai, y_xoai):
            y_xoai = 0
            x_xoai = random.randint(0, chieu_dai - 60)

        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
        w.blit(score_text, (10, 10))
        w.blit(lives_text, (chieu_dai - 150, 10))

    pygame.display.update()
    fpsClock.tick(FPS)
