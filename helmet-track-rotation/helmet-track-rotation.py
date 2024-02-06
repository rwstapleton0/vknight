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
    return image, image.get_rect()

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
pygame.init()

# Initialize required elements/environment
VID_CAP = cv.VideoCapture(0)
window_size = (VID_CAP.get(cv.CAP_PROP_FRAME_WIDTH), VID_CAP.get(cv.CAP_PROP_FRAME_HEIGHT)) # width by height
screen = pygame.display.set_mode(window_size)

class HelmetBody(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.image, self.rect = load_image("helmet_body_a.png", pos, 0.5)
        self.orig_image = self.image

class FaceGuard(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.image, self.frame = load_image("face_guard_a.png", pos, 0.5)
        self.orig_image = self.image

        self.pos = Vector2(pos[0] -9, pos[1] - 8)  # The original center position/pivot point.
        self.orig_pos = Vector2(self.pos)
        self.offset = Vector2(-130, 34)  # We shift the sprite 50 px to the right.
        self.angle = 0
    
    def update(self):
        # self.angle += 2
        self.rotate()
    
    def shake(self):
        ran_range_x = (-1,1)
        ran_range_y = (-1,1)
        if self.pos.x > self.orig_pos.x + 5:
            ran_range_x = (-1, 0)
        elif self.pos.x < self.orig_pos.x - 5:
            ran_range_x = (0, 1)
        if self.pos.y > self.orig_pos.y + 5:
            ran_range_y = (-1, 0)
        elif self.pos.y < self.orig_pos.y - 5:
            ran_range_y = (0, 1)
         
        self.pos += (random.randint(ran_range_x[0], ran_range_x[1]), 
            random.randint(ran_range_y[0], ran_range_y[1]))

    def stop_shake(self):
        self.pos = Vector2(self.orig_pos)

    def rotate(self): # Fix this is a bit
        """Rotate the image of the sprite around a pivot point."""
        # Rotate the image.
        self.image = pygame.transform.rotozoom(self.orig_image, -self.angle, 1)
        # Rotate the offset vector.
        offset_rotated = self.offset.rotate(self.angle)
        # Create a new rect with the center of the sprite + the offset.
        self.rect = self.image.get_rect(center=self.pos+offset_rotated)


# Helmet sprites
screen_center = (window_size[0] // 2, window_size[1] // 2)

helmet_body = HelmetBody(screen_center)
face_guard = FaceGuard(screen_center)

all_sprites = pygame.sprite.Group(helmet_body, face_guard)

# Game loop
game_clock = time.time()
game_is_running = True

with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:
    while game_is_running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_is_running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_is_running = False

        # Get frame
        ret, frame = VID_CAP.read()
        if not ret:
            print("Empty frame, continuing...")
            continue

        # frame.flags.writeable = False
        # frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        result = face_mesh.process(frame)
        # frame.flags.writeable = True
        # frame = cv.flip(frame, 1).swapaxes(0,1)
        # pygame.surfarray.blit_array(screen, frame)

        if result.multi_face_landmarks and len(result.multi_face_landmarks) > 0:
            face = result.multi_face_landmarks[0]
            if face.landmark[15].y - face.landmark[11].y > 0.036: 
                face_guard.shake()
            else:
                face_guard.stop_shake()
        
        # Screen Functions 
        all_sprites.update()

        screen.fill((125, 220, 232))
        all_sprites.draw(screen)
        pygame.display.flip()

    VID_CAP.release()
    cv.destroyAllWindows()
    pygame.quit()
    sys.exit()