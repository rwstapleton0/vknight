import sys, time, random, pygame
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



pygame.init()



window_size = (600,400)
screen = pygame.display.set_mode(window_size)


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
        self.anim_state = 0
        self.rot_speed = 0
        self.is_open = False
        self.finished_anim = True

    def update(self):

        if self.is_open:
            self.anim_open()
        elif not self.is_open:
            self.anim_close()

        self.angle += self.rot_speed

        self.image = pygame.transform.rotozoom(self.orig_image, -self.angle, 1)
        self.offset_rotated = self.rot_offset.rotate(self.angle)

        self.rect = self.image.get_rect(center=self.pos+self.offset_rotated+self.offset)

    def anim_open(self):
        if (self.anim_state == 0):
            self.rot_speed = 0
        elif (self.anim_state == 1):
            self.rot_speed = 8
            if (self.angle > 100): 
                self.anim_state = 2
        elif (self.anim_state == 2):
            self.rot_speed = -7
            if (self.angle < 70): 
                self.anim_state = 3
        elif (self.anim_state == 3):
            self.rot_speed = 6
            if (self.angle > 95): 
                self.anim_state = 4
        elif (self.anim_state == 4):
            self.rot_speed = -5
            if (self.angle < 75): 
                self.anim_state = 5
        elif (self.anim_state == 5):
            self.rot_speed = 4
            if (self.angle > 90): 
                self.anim_state = 6
        elif (self.anim_state == 6):
            self.rot_speed = -3
            if (self.angle < 80): 
                self.anim_state = 7
        elif (self.anim_state == 7):
            self.rot_speed = 2
            if (self.angle > 85): 
                self.anim_state = 8
        elif (self.anim_state == 8):
            self.rot_speed = -1
            if (self.angle < 80): 
                self.anim_state = 0

    def anim_close(self):
        if (self.anim_state == 0):
            self.rot_speed = 0
        elif (self.anim_state == 1):
            self.rot_speed = -8
            if (self.angle < 4): 
                self.anim_state = 2
        elif (self.anim_state == 2):
            self.rot_speed = 4
            if (self.angle > 5): 
                self.anim_state = 3
        elif (self.anim_state == 3):
            self.rot_speed = -1
            if (self.angle < 0):
                self.angle = 0
                self.anim_state = 0

    def set_is_open(self):
        self.anim_state = 1
        self.is_open = not self.is_open
        print(self.is_open)

class HelmetFull():

    def __init__(self, pos):
        self.pos = Vector2(pos)

        self.helmet_body = HelmetBody(self.pos)
        self.face_guard = FaceGuard(self.pos)

        self.helmet_sprites = pygame.sprite.Group(self.helmet_body, self.face_guard)


    def update(self):
        # self.pos.x += 1

        self.helmet_sprites.update()

    def draw(self, screen):
        self.helmet_sprites.draw(screen)
    
    def set_is_open(self):
        self.face_guard.set_is_open()


helmet = HelmetFull((300,200))

game_clock = pygame.time.Clock()
game_is_running = True

while game_is_running:
    
    game_clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_is_running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            game_is_running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            helmet.set_is_open()


    # Screen Functions
    helmet.update()

    screen.fill((125, 220, 232))
    
    helmet.draw(screen)

    pygame.display.flip()
    
pygame.quit()
sys.exit()