import pygame, sys
from pygame.locals import *
import random

# Khởi tạo Pygame
pygame.init()
pygame.mixer.init()

# Thiết lập cửa sổ game
chieu_dai = 800
chieu_rong = 500
w = pygame.display.set_mode((chieu_dai, chieu_rong))
pygame.display.set_caption('Flappy Bird')

# Màu sắc
BLACK = (0, 0, 0)

# Tải âm thanh
hit_sound = pygame.mixer.Sound("hit.wav")  # Thay "hit.wav" bằng tên file âm thanh của bạn
score_sound = pygame.mixer.Sound("score.wav")  # Thay "score.wav" bằng tên file âm thanh của bạn

# Tải nhạc nền
pygame.mixer.music.load("nhacnen.mp3")  # Thay "nhacnen.mp3" bằng tên file nhạc nền của bạn
pygame.mixer.music.play(-1) # Phát nhạc nền lặp lại

# Tải hình ảnh
anh_nen = pygame.image.load('bg2.png').convert()
anh_nen = pygame.transform.scale(anh_nen, (chieu_dai, chieu_rong))
chim1 = pygame.image.load('chim2.png').convert_alpha()
chim1 = pygame.transform.scale(chim1, (80, 70))
cot = pygame.image.load('nui.png').convert_alpha()
cot = pygame.transform.scale(cot, (100, 250))

# Biến game
x1 = 50
y1 = chieu_rong // 2  # Chim bắt đầu ở giữa màn hình theo chiều dọc
toc_do_roi = 0
trong_luc = 0.3
diem_so = 0
cap_do = 1
toc_do_cot = 3
khoang_cach_cot = 300
danh_sach_cot = []
game_started = False  # Biến kiểm tra game đã bắt đầu chưa

# Tạo chướng ngại vật
def tao_cot():
    chieu_cao_ngau_nhien = random.randint(100, 350)
    cot_tren = cot.get_rect(bottomleft=(chieu_dai, chieu_cao_ngau_nhien - khoang_cach_cot))
    cot_duoi = cot.get_rect(topleft=(chieu_dai, chieu_cao_ngau_nhien))
    return cot_tren, cot_duoi # Trả về tuple gồm 2 giá trị

# Hiển thị điểm số
font = pygame.font.SysFont(None, 50)
def hien_thi_diem(diem_so):
    text = font.render("Điểm: " + str(diem_so), True, BLACK)
    w.blit(text, (10, 10))

# Khởi tạo danh sách cột
danh_sach_cot.append(tao_cot())

# Khoi tao khung thoi gian
FPS = 60
fpsClock = pygame.time.Clock()

# Vòng lặp game
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if not game_started:  # Kiểm tra nếu game chưa bắt đầu
                    game_started = True
                    toc_do_roi = -8  # Bắt đầu cho chim bay lên
                else:
                    toc_do_roi = -8

    if game_started:  # Chỉ xử lý logic game khi game đã bắt đầu
        # Áp dụng trọng lực
        toc_do_roi += trong_luc
        y1 += toc_do_roi

        # Di chuyển cột
        for cot_tren, cot_duoi in danh_sach_cot:
            cot_tren.x -= toc_do_cot
            cot_duoi.x -= toc_do_cot

            # Tạo cột mới
            if cot_tren.right < 0:
                danh_sach_cot.pop(0)
                danh_sach_cot.append(tao_cot())
                diem_so += 1
                score_sound.play()  # Phát âm thanh khi ăn điểm

        # Kiểm tra va chạm
        chim_rect = chim1.get_rect(topleft=(x1, y1))
        for cot_tren, cot_duoi in danh_sach_cot:
            if chim_rect.colliderect(cot_tren) or chim_rect.colliderect(cot_duoi) or y1 < 0 or y1 > chieu_rong:
                hit_sound.play()  # Phát âm thanh va chạm
                running = False

        # Tăng độ khó (cấp độ)
        if diem_so % 5 == 0 and diem_so > 0:
            cap_do += 1
            toc_do_cot += 0.5
            if khoang_cach_cot > 200:
                khoang_cach_cot -= 20

    # Vẽ hình ảnh
    w.blit(anh_nen, (0, 0))
    for cot_tren, cot_duoi in danh_sach_cot:
        w.blit(cot, cot_tren)
        w.blit(cot, cot_duoi)
    w.blit(chim1, (x1, y1))
    hien_thi_diem(diem_so)

    # Cập nhật màn hình
    pygame.display.update()
    fpsClock.tick(FPS)

pygame.quit()
sys.exit()