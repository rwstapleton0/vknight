import sys, time, random, pygame
from collections import deque
import cv2 as cv, mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
pygame.init()

# Initialize required elements/environment
VID_CAP = cv.VideoCapture(0)
window_size = (VID_CAP.get(cv.CAP_PROP_FRAME_WIDTH), VID_CAP.get(cv.CAP_PROP_FRAME_HEIGHT)) # width by height
screen = pygame.display.set_mode(window_size)

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

        screen.fill((125, 220, 232))

        frame.flags.writeable = False
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        result = face_mesh.process(frame)

        # Outline / breaks if cant find face
        facelandmarks = []
        for facial_landmarks in result.multi_face_landmarks:
            for i in range(0, 468):
                pt1 = facial_landmarks.landmark[i]
                x = int(pt1.x * window_size[0])
                y = int(pt1.y * window_size[1])
                facelandmarks.append([x, y])
        landmarks = np.array(facelandmarks, np.int32)
        
        convexhull = cv.convexHull(landmarks)

        # Create a mask
        mask = np.zeros((int(window_size[1]), int(window_size[0])), np.uint8)
        cv.fillConvexPoly(mask, convexhull, 255)

        green_bg = np.zeros((int(window_size[1]), int(window_size[0]), 3), dtype=np.uint8)
        green_bg[:] = (0, 255, 0)  # Green in BGR format

        # Use the mask to blend the face with the green background
        for i in range(3):  # loop through each channel (BGR)
            green_bg[:, :, i] = cv.bitwise_and(frame[:, :, i], frame[:, :, i], mask=mask) + \
                                cv.bitwise_and(green_bg[:, :, i], green_bg[:, :, i], mask=~mask)

        # Convert to a format suitable for Pygame
        face_extracted = cv.cvtColor(green_bg, cv.COLOR_BGR2RGB)
        face_extracted = np.rot90(face_extracted)

        # Display in Pygame window
        surf = pygame.surfarray.make_surface(face_extracted)
        screen.blit(surf, (0, 0))
        pygame.display.flip()


    VID_CAP.release()
    cv.destroyAllWindows()
    pygame.quit()
    sys.exit()