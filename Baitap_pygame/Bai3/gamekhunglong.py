import pygame
import random

# Khởi tạo pygame
pygame.init()

# Cấu hình kích thước cửa sổ game
WINDOWWIDTH = 800
WINDOWHEIGHT = 400
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

# Cấu hình màu sắc và tốc độ
SPEED_GROUND = 5
DISTANCE_MIN = 300
DISTANCE_MAX = 600
Y_CATUS = 300
Y_BIRD_1, Y_BIRD_2, Y_BIRD_3 = 250, 200, 150
FPS = 30

# Khởi tạo clock
fpsClock = pygame.time.Clock()

# Tạo nhân vật T-Rex
class TRex():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = pygame.image.load('img/tRex.png')
        self.surface = pygame.Surface(self.img.get_size(), pygame.SRCALPHA)
        self.surface.blit(self.img, (0, 0))
        self.jump = False
        self.jump_speed = -15
        self.gravity = 1

    def update(self):
        if self.jump:
            self.y += self.jump_speed
            self.jump_speed += self.gravity
            if self.y >= Y_CATUS:
                self.y = Y_CATUS
                self.jump = False
                self.jump_speed = -15

    def draw(self):
        DISPLAYSURF.blit(self.surface, (self.x, self.y))

# Chướng ngại vật: Xương rồng
class Catus():
    def __init__(self, x, y, img_index):
        self.x = x
        self.y = y
        self.img = pygame.image.load(f'img/catus_{img_index}.png')
        self.surface = pygame.Surface(self.img.get_size(), pygame.SRCALPHA)
        self.surface.blit(self.img, (0, 0))

    def update(self, speed):
        self.x -= int(speed)

    def draw(self):
        DISPLAYSURF.blit(self.surface, (self.x, self.y))

# Chướng ngại vật: Chim
class Bird():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = pygame.image.load('img/bird.png')
        self.surface = pygame.Surface(self.img.get_size(), pygame.SRCALPHA)
        self.surface.blit(self.img, (0, 0))

    def update(self, speed):
        self.x -= int(speed)

    def draw(self):
        DISPLAYSURF.blit(self.surface, (self.x, self.y))

# Chướng ngại vật: Tảng đá
class Rock():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = pygame.image.load('img/rock.png')
        self.surface = pygame.Surface(self.img.get_size(), pygame.SRCALPHA)
        self.surface.blit(self.img, (0, 0))

    def update(self, speed):
        self.x -= int(speed)

    def draw(self):
        DISPLAYSURF.blit(self.surface, (self.x, self.y))

# Chướng ngại vật: Mưa thiên thạch
class Meteor():
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.img = pygame.image.load('img/meteor.png')
        self.speed = speed
        self.surface = pygame.Surface(self.img.get_size(), pygame.SRCALPHA)
        self.surface.blit(self.img, (0, 0))

    def update(self):
        self.y += self.speed  # Rơi xuống
        if self.y > WINDOWHEIGHT:  # Nếu ra khỏi màn hình thì reset
            self.y = -50
            self.x = random.randint(0, WINDOWWIDTH)

    def draw(self):
        DISPLAYSURF.blit(self.surface, (self.x, self.y))

# Danh sách vật cản: Xương rồng, Chim, Tảng đá, Thiên thạch
class ListCatusAndBirds():
    def __init__(self):
        self.list = []
        for i in range(0, 3):
            self.list.append(Catus(500 + WINDOWWIDTH + random.randint(DISTANCE_MIN, DISTANCE_MAX) * i, Y_CATUS,
                                   random.randint(0, 3)))
        self.list.append(Meteor(random.randint(0, WINDOWWIDTH), -50, random.randint(5, 10)))  # Thêm thiên thạch
        self.speed = SPEED_GROUND

    def update(self, score):
        self.speed = SPEED_GROUND * (1 + score / 500)
        if self.speed > SPEED_GROUND * 2:
            self.speed = SPEED_GROUND * 2
        for i in range(len(self.list)):
            if isinstance(self.list[i], Meteor):
                self.list[i].update()  # Thiên thạch rơi thẳng xuống
            else:
                self.list[i].update(self.speed)

        # Kiểm tra nếu vật cản ra khỏi màn hình thì thêm vật cản mới
        if self.list[0].x < -132 or (isinstance(self.list[0], Meteor) and self.list[0].y > WINDOWHEIGHT):
            self.list.pop(0)
            if self.speed > SPEED_GROUND * 1.5:
                rand = random.randint(0, 5)
                if rand == 5:
                    self.list.append(Bird(self.list[1].x + random.randint(DISTANCE_MIN + 200, DISTANCE_MAX + 100),
                                          random.choice((Y_BIRD_1, Y_BIRD_2, Y_BIRD_3))))
                elif rand == 4:
                    self.list.append(Rock(self.list[1].x + random.randint(DISTANCE_MIN, DISTANCE_MAX), Y_CATUS))
                else:
                    self.list.append(
                        Catus(self.list[1].x + random.randint(DISTANCE_MIN + 100, DISTANCE_MAX + 100), Y_CATUS,
                              random.randint(0, 4)))
            else:
                self.list.append(
                    Catus(self.list[1].x + random.randint(DISTANCE_MIN, DISTANCE_MAX), Y_CATUS, random.randint(0, 3)))
                self.list.append(Meteor(random.randint(0, WINDOWWIDTH), -50, random.randint(5, 10)))  # Thêm thiên thạch

    def draw(self):
        for i in range(len(self.list)):
            self.list[i].draw()

# Kiểm tra va chạm
def isCollision(tRex, ls):
    tRexMask = pygame.mask.from_surface(tRex.surface)
    for obstacle in ls.list:
        obstacle_mask = pygame.mask.from_surface(obstacle.surface)
        if isinstance(obstacle, Rock) or isinstance(obstacle, Catus) or isinstance(obstacle, Bird):
            result = tRexMask.overlap(obstacle_mask, (obstacle.x - tRex.x, obstacle.y - tRex.y))
            if result:
                return True
        elif isinstance(obstacle, Meteor):  # Thiên thạch rơi thẳng xuống
            result = tRexMask.overlap(obstacle_mask, (obstacle.x - tRex.x, obstacle.y - tRex.y))
            if result:
                return True
    return False

# Vòng lặp chính của trò chơi
def game():
    score = 0
    tRex = TRex(50, Y_CATUS)
    listCatusBirds = ListCatusAndBirds()

    running = True
    while running:
        DISPLAYSURF.fill((255, 255, 255))  # Màu nền trắng

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and tRex.y == Y_CATUS:
                    tRex.jump = True

        # Cập nhật
        tRex.update()
        listCatusBirds.update(score)

        # Vẽ
        tRex.draw()
        listCatusBirds.draw()

        # Kiểm tra va chạm
        if isCollision(tRex, listCatusBirds):
            running = False  # Kết thúc trò chơi nếu va chạm

        # Tăng điểm
        score += 1
        pygame.display.update()
        fpsClock.tick(FPS)

game()
pygame.quit()
