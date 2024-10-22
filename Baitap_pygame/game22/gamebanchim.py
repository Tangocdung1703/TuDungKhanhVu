import pygame, sys
from pygame.locals import *
import random

# Khởi tạo Pygame
pygame.init()

# -------- Cài đặt --------
chieu_dai = 1000  # Chiều dài cửa sổ
chieu_rong = 700  # Chiều cao cửa sổ
w = pygame.display.set_mode((chieu_dai, chieu_rong))  # Tạo cửa sổ game
pygame.display.set_caption('Bắn Chim')

# -------- Màu sắc --------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# -------- Font chữ --------
font = pygame.font.SysFont(None, 36)  # Chọn font chữ mặc định, kích thước 36
font_game_over = pygame.font.SysFont(None, 60)

# -------- Hình ảnh --------
anh_nen = pygame.image.load('bg2.png').convert()
anh_nen = pygame.transform.scale(anh_nen, (chieu_dai, chieu_rong))
chim1 = pygame.image.load('chim1.png').convert_alpha()
chim1 = pygame.transform.scale(chim1, (80, 70))
chim2 = pygame.image.load('chim2.png').convert_alpha()
chim2 = pygame.transform.scale(chim2, (80, 70))
nui = pygame.image.load('nui.png').convert_alpha()
nui = pygame.transform.scale(nui, (250, 250))
vien_dan_img = pygame.Surface((5, 10))
vien_dan_img.fill(BLACK)

# -------- Âm thanh (nếu cần) --------
# am_thanh_ban = pygame.mixer.Sound('ban.wav')

# -------- Lớp Chim --------
class Chim(pygame.sprite.Sprite):
    def __init__(self, anh, toc_do):
        super().__init__()
        self.image = anh
        self.rect = self.image.get_rect()
        self.toc_do = toc_do
        self.reset()

    def update(self):
        self.rect.x -= self.toc_do
        if self.rect.x < -self.rect.width:
            self.reset()

    def reset(self):
        self.rect.x = random.randrange(chieu_dai, chieu_dai + 100)
        self.rect.y = random.randrange(0, chieu_rong - self.rect.height)

# -------- Lớp Viên Đạn --------
class VienDan(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = vien_dan_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.toc_do = 10

    def update(self):
        self.rect.x += self.toc_do
        if self.rect.x > chieu_dai:
            self.kill()

# -------- Khởi tạo biến --------
x_nguoi_choi = 50
y_nguoi_choi = chieu_rong - 120
toc_do_nguoi_choi = 5
diem_so = 0
level = 1
toc_do_chim_ban_dau = 1
so_luong_chim = 5
game_over = False

# -------- Nhóm sprite --------
tat_ca_sprite = pygame.sprite.Group()
dan_nhom = pygame.sprite.Group()
chim_nhom = pygame.sprite.Group()

# -------- Tạo chim ban đầu --------
for _ in range(so_luong_chim):
    chim = Chim(chim1 if random.randint(0, 1) == 0 else chim2, toc_do_chim_ban_dau)
    tat_ca_sprite.add(chim)
    chim_nhom.add(chim)

# -------- Khung thời gian --------
FPS = 60
fpsClock = pygame.time.Clock()

def hien_thi_thong_bao(message, font, color, x, y):
    """Hàm hiển thị thông báo trên màn hình"""
    text_surface = font.render(message, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    w.blit(text_surface, text_rect)

def xu_ly_nut_choi_lai():
    """Xử lý sự kiện khi nhấn nút Chơi lại"""
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if nut_choi_lai_rect.collidepoint(event.pos):
                    # Reset game
                    global diem_so, level, game_over
                    diem_so = 0
                    level = 1
                    game_over = False
                    # Tạo lại chim
                    for chim in chim_nhom:
                        chim.kill()
                    for _ in range(so_luong_chim):
                        chim = Chim(chim1 if random.randint(0, 1) == 0 else chim2,
                                  toc_do_chim_ban_dau + level)
                        tat_ca_sprite.add(chim)
                        chim_nhom.add(chim)
                    return  # Quay lại vòng lặp chính

        pygame.display.update()
        fpsClock.tick(FPS)

# -------- Vòng lặp chính --------
running = True
while running:
    # -------- Xử lý sự kiện --------
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                vien_dan = VienDan(x_nguoi_choi + 50, y_nguoi_choi + 25)
                tat_ca_sprite.add(vien_dan)
                dan_nhom.add(vien_dan)
                # am_thanh_ban.play()

    if not game_over:
        # -------- Xử lý phím --------
        keys = pygame.key.get_pressed()
        if keys[K_UP] and y_nguoi_choi > 0:
            y_nguoi_choi -= toc_do_nguoi_choi
        if keys[K_DOWN] and y_nguoi_choi < chieu_rong - chim1.get_height():
            y_nguoi_choi += toc_do_nguoi_choi

        # -------- Cập nhật sprite --------
        tat_ca_sprite.update()

        # -------- Kiểm tra va chạm --------
        va_cham = pygame.sprite.groupcollide(chim_nhom, dan_nhom, True, True)
        for chim_bi_ban in va_cham:
            diem_so += 5  # Tăng 5 điểm cho mỗi con chim bị bắn
            # Tạo chim mới thay thế chim bị bắn
            chim_moi = Chim(chim1 if random.randint(0, 1) == 0 else chim2,
                          toc_do_chim_ban_dau + level)
            tat_ca_sprite.add(chim_moi)
            chim_nhom.add(chim_moi)

        # -------- Kiểm tra va chạm với người chơi --------
        va_cham_nguoi_choi = pygame.sprite.spritecollide(
            pygame.sprite.Sprite(chim1.get_rect(topleft=(x_nguoi_choi, y_nguoi_choi))),
            chim_nhom,
            False
        )

        if va_cham_nguoi_choi:  # Kiểm tra danh sách va chạm
            game_over = True

        # -------- Tăng cấp độ --------
        if diem_so >= 20 * level:
            level += 1
            # Tăng tốc độ chim cho level mới (có thể điều chỉnh giá trị tăng)
            for chim in chim_nhom:
                chim.toc_do = toc_do_chim_ban_dau + level

        # -------- Duy trì số lượng chim --------
        if len(chim_nhom) < 5:
            for _ in range(5 - len(chim_nhom)):
                chim = Chim(chim1 if random.randint(0, 1) == 0 else chim2, toc_do_chim_ban_dau + level)
                tat_ca_sprite.add(chim)
                chim_nhom.add(chim)

    # -------- Vẽ --------
    w.blit(anh_nen, (0, 0))
    w.blit(nui, (300, 200))
    w.blit(chim1, (x_nguoi_choi, y_nguoi_choi))  # Vẽ "người chơi"
    tat_ca_sprite.draw(w)

    # Hiển thị điểm số
    diem_text = font.render("Điểm: " + str(diem_so), True, WHITE)
    w.blit(diem_text, (10, 10))

    # Hiển thị level
    level_text = font.render("Level: " + str(level), True, WHITE)
    w.blit(level_text, (chieu_dai - level_text.get_width() - 10, 10))

    if game_over:
        hien_thi_thong_bao("Bạn đã chết!", font_game_over, RED, chieu_dai // 2, chieu_rong // 2 - 50)
        nut_choi_lai_rect = pygame.Rect(chieu_dai // 2 - 100, chieu_rong // 2, 200, 50)
        pygame.draw.rect(w, WHITE, nut_choi_lai_rect)
        hien_thi_thong_bao("Chơi lại", font, BLACK, chieu_dai // 2, chieu_rong // 2 + 25)
        xu_ly_nut_choi_lai()

    # -------- Cập nhật màn hình --------
    pygame.display.flip()

    # -------- Giới hạn FPS --------
    fpsClock.tick(FPS)

pygame.quit()
sys.exit()