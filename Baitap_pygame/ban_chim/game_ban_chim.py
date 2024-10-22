import pygame
import random

# Khởi tạo Pygame
pygame.init()

# Kích thước màn hình
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Tên cửa sổ
pygame.display.set_caption("Game Bắn Chim")

# Màu sắc
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Load ảnh chim và đạn
bird_img = pygame.image.load('chim1.png')
bird_img = pygame.transform.scale(bird_img, (80,70))
bullet_img = pygame.image.load('bullet.png')
bullet_img = pygame.transform.scale(bullet_img, (20,40))

# load bg
background_img = pygame.image.load('bg2.jpg')
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

# Tạo lớp Chim
class Bird:
    def __init__(self):
        self.x = random.randint(-50, 0)
        self.y = random.randint(50, screen_height // 2)
        self.speed = random.randint(2, 5)

    def move(self):
        self.x += self.speed
        if self.x > screen_width:
            self.x = 0
            self.y = random.randint(50, screen_height // 2)

    def draw(self, screen):
        screen.blit(bird_img, (self.x, self.y))

# Tạo lớp Đạn
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 7

    def move(self):
        self.y -= self.speed

    def draw(self, screen):
        screen.blit(bullet_img, (self.x, self.y))

# Hàm kiểm tra va chạm
def check_collision(bullet, bird):
    return bird.x < bullet.x < bird.x + bird_img.get_width() and bird.y < bullet.y < bird.y + bird_img.get_height()

# Khởi tạo biến
running = True
birds = [Bird() for _ in range(5)]
bullets = []
score = 0
font = pygame.font.SysFont(None, 55)

# Vòng lặp chính của trò chơi
while running:
    screen.fill(WHITE)

    # Kiểm tra sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            bullets.append(Bullet(x, screen_height - 50))
    
    screen.blit(background_img,(0,0))

    # Di chuyển và vẽ chim
    for bird in birds:
        bird.move()
        bird.draw(screen)

    # Di chuyển và vẽ đạn
    for bullet in bullets[:]:
        bullet.move()
        bullet.draw(screen)
        if bullet.y < 0:
            bullets.remove(bullet)
        for bird in birds:
            if check_collision(bullet, bird):
                birds.remove(bird)
                bullets.remove(bullet)
                birds.append(Bird())  # Thêm một con chim mới
                score += 1
                break

    # Hiển thị điểm số
    score_text = font.render(f"Score: {score}", True, RED)
    screen.blit(score_text, (10, 10))

    # Cập nhật màn hình
    pygame.display.flip()
    pygame.time.Clock().tick(60)

# Thoát khỏi Pygame
pygame.quit()
