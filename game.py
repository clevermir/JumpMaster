import pygame
from pygame.locals import *
import sys
import random

# Pygame-ni ishga tushirish
pygame.init()

# Oyin uchun umumiy ozgaruvchilar
vec = pygame.math.Vector2
HEIGHT = 350
WIDTH = 700
ACC = 0.3
FRIC = -0.10
FPS = 60
FPS_CLOCK = pygame.time.Clock()
COUNT = 0

# Ekran sozlamalari
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mening O‘yinim")

# Fon sinfi
class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.bgimage = pygame.image.load("Background.png")  # Fon rasmi
        self.bgY = 0
        self.bgX = 0

    def render(self):
        displaysurface.blit(self.bgimage, (self.bgX, self.bgY))

# Yer sinfi
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Ground.png")  # Yer rasmi
        self.rect = self.image.get_rect(center=(350, 350))

    def render(self):
        displaysurface.blit(self.image, (self.rect.x, self.rect.y))

# Oyinchi sinfi
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player_Sprite_R.png")  # Oyinchi rasmi
        self.rect = self.image.get_rect()
        self.vx = 0
        self.pos = vec((340, 240))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.direction = "RIGHT"

    def move(self):
        self.acc = vec(0, 0.5)  # Gravitatsiya tasiri
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
            self.direction = "LEFT"
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
            self.direction = "RIGHT"
        
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        
        self.rect.midbottom = self.pos

    def update(self):
        self.move()

    def attack(self):
        pass  # Hujum funksiyasini keyin qo‘shishingiz mumkin

    def jump(self):
        if self.rect.bottom >= 350:  # Yerda bo‘lsa sakrashga ruxsat
            self.vel.y = -10

# Ob’ektlarni yaratish
background = Background()
ground = Ground()
player = Player()

# Asosiy oyin tsikli
while True:
    for event in pygame.event.get():
        if event.type == QUIT:  # Oynani yopish
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Boshliq tugmasi bilan sakrash
                player.jump()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass  # Sichqoncha bilan biror harakat qoshish mumkin

    # Yangilash va chizish
    player.update()
    background.render()
    ground.render()
    displaysurface.blit(player.image, player.rect)

    # Ekran yangilash
    pygame.display.update()
    FPS_CLOCK.tick(FPS)