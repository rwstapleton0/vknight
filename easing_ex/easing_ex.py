import sys, time, random, pygame, math

def easeOutElastic(x):
        c4 = (2 * math.pi) / 3

        if x == 0:
            return 0
        elif x == 1:
            return 1
        else:
            return math.pow(2, -10 * x) * math.sin((x * 10 - 0.75) * c4) + 1

pygame.init()

window_size = (600,400)
screen = pygame.display.set_mode(window_size)

game_clock = pygame.time.Clock()
game_is_running = True

ease = 0


while game_is_running:
    
    game_clock.tick(1000)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_is_running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            game_is_running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            ease = 0.1

    screen.fill((125, 220, 232))

    ease = easeOutElastic(ease)

    size = 50

    pygame.draw.circle(screen, (100,0,100), (300, 200), size * ease)

    pygame.display.flip()
    
pygame.quit()
sys.exit()













# main_dir = os.path.split(os.path.abspath(__file__))[0]
# data_dir = os.path.join(main_dir, "data")

# def load_image(name, pos, scale=1):
#     fullname = os.path.join(data_dir, name)
#     image = pygame.image.load(fullname).convert_alpha()

#     size = image.get_size()
#     size = (size[0] * scale, size[1] * scale)
#     image = pygame.transform.scale(image, size)
#     return image, image.get_rect(center=pos)

# class FaceGuard(pygame.sprite.Sprite):

#     def __init__(self, pos):
#         super().__init__()

#         self.image, self.rect = load_image("face_guard_a.png", pos, 0.5)
#         self.orig_image = self.image

#         self.pos = pos
#         self.offset = Vector2(92, -2)

#         self.rot_offset = Vector2(-130, 34)

#         self.angle = 0
#         self.is_open = False

#     def update(self):

#         pygame.draw.circle()

#         self.angle += self.rot_speed

#         self.image = pygame.transform.rotozoom(self.orig_image, -self.angle, 1)
#         self.offset_rotated = self.rot_offset.rotate(self.angle)

#         self.rect = self.image.get_rect(center=self.pos+self.offset_rotated+self.offset)

#     def easeOutElastic(x: number):
#         c4 = (2 * math.pi) / 3

#         if x === 0:
#             return 0
#         elif x === 1:
#             return 1
#         else:
#             return math.pow(2, -10 * x) * math.sin((x * 10 - 0.75) * c4) + 1

#     def set_is_open(self):
#         self.is_open = not self.is_open
