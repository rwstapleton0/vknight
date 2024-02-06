import sys, time, random, pygame, math
from pygame.math import Vector2
from collections import deque
import cv2 as cv, mediapipe as mp
import os

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")

def load_image(name, pos, scale=1):
    fullname = os.path.join(data_dir, name)
    image = pygame.image.load(fullname).convert_alpha()

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pygame.transform.scale(image, size)
    return image, image.get_rect(center=pos)

def easeOutElastic(x):
    c4 = (2 * math.pi) / 3
    if x == 0:
        return 0
    elif x == 1:
        return 1
    else:
        return math.pow(2, -10 * x) * math.sin((x * 10 - 0.5) * c4) + 1

def easeOutBounce(x):
    n1 = 7.5625
    d1 = 2.75
    
    if x < 1 / d1:
        return n1 * x * x
    elif x < 2 / d1:
        x -= 1.5 / d1
        return n1 * x * x + 0.75
    elif x < 2.5 / d1:
        x -= 2.25 / d1
        return n1 * x * x + 0.9375
    else:
        x -= 2.625 / d1
        return n1 * x * x + 0.984375


class HelmetBody(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.image, self.rect = load_image("helmet_body_a.png", pos, 0.5)
        self.pos = pos

    def update(self):
        self.rect = self.image.get_rect(center=self.pos)

class FaceGuard(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.image, self.rect = load_image("face_guard_a.png", pos, 0.5)
        self.orig_image = self.image

        self.pos = pos
        self.offset = Vector2(92, -2)
        self.rot_offset = Vector2(-130, 34)

        self.angle = 0
        self.duration = 2
        self.start_time = 0
        self.open_anim = False

    def update(self):

        self.image = pygame.transform.rotozoom(self.orig_image, -self.angle, 1)
        self.offset_rotated = self.rot_offset.rotate(self.angle)

        elapsed = (pygame.time.get_ticks() - self.start_time) / 1000
        self.x = min(elapsed / self.duration, 1)

        if self.open_anim:
            self.angle = 90 * easeOutElastic(self.x)
        else:
            self.angle = 90 * (1 - easeOutBounce(self.x ** 2))

        self.rect = self.image.get_rect(center=self.pos+self.offset_rotated+self.offset)

    def start_anim(self):
        self.open_anim = not self.open_anim
        self.start_time = pygame.time.get_ticks()

class HelmetFull():

    def __init__(self, pos):
        self.pos = Vector2(pos)

        self.helmet_body = HelmetBody(self.pos)
        self.face_guard = FaceGuard(self.pos)

        self.helmet_sprites = pygame.sprite.Group(self.helmet_body, self.face_guard)

    def update(self):
        self.helmet_sprites.update()

    def draw(self, screen):
        self.helmet_sprites.draw(screen)

    def start_anim(self):
        self.face_guard.start_anim()


pygame.init()

window_size = (600,400)
screen = pygame.display.set_mode(window_size)


helmet = HelmetFull((300,200))

game_clock = pygame.time.Clock()
game_is_running = True

run_anim = False

while game_is_running:
    
    game_clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_is_running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            game_is_running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            helmet.start_anim()
            run_anim = True
        

    screen.fill((125, 220, 232))

    helmet.update()
    helmet.draw(screen)

    pygame.display.flip()
    
pygame.quit()
sys.exit()