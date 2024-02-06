import math
import pygame
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

class FaceGuard(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.image, self.rect = load_image("face_guard_a.png", pos, 0.5)
        self.angle = 0
        self.is_open = False

    def update(self, angle):
        self.rot_center(angle)

    def rot_center(self, angle):
        """rotate an image while keeping its center"""
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        
    def set_is_open(self):
        self.is_open = not self.is_open


# Pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

face_guard = FaceGuard((400,300))

helmet_sprites = pygame.sprite.Group(face_guard)

# Animation variables
duration = 2  # Duration of the animation in seconds
start_time = pygame.time.get_ticks()
angle = 0  # Initial rotation angle

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # Calculate elapsed time
    elapsed = (pygame.time.get_ticks() - start_time) / 1000  # Convert milliseconds to seconds

    # Normalize elapsed time for the easing function
    x = min(elapsed / duration, 1)

    # Apply easing function for rotation
    angle = 90 * easeOutElastic(x)  # Example: rotate from 0 to 360 degrees

    print(angle)

    screen.fill((125, 220, 232))


    face_guard.update(angle)
    helmet_sprites.draw(screen)


    pygame.display.flip()
    clock.tick(60)  # Run at 60 frames per second

pygame.quit()