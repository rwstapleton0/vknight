
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import matplotlib.pyplot as plt


def draw_landmarks_on_image(rgb_image, detection_result):
  face_landmarks_list = detection_result.face_landmarks
  annotated_image = np.copy(rgb_image)

  # Loop through the detected faces to visualize.
  for idx in range(len(face_landmarks_list)):
    face_landmarks = face_landmarks_list[idx]

    # Draw the face landmarks.
    face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    face_landmarks_proto.landmark.extend([
      landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in face_landmarks
    ])

    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp.solutions.drawing_styles
        .get_default_face_mesh_contours_style())

  return annotated_image

import cv2

  # STEP 1: Import the necessary modules.
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class FaceDecector:
    detection_result = None
    def __init__(self):
        model_PATH = '/home/yebooty/Programs/mediapipe/face-landmark-image/face_landmarker_v2_with_blendshapes.task'

        options = vision.FaceLandmarkerOptions(
            base_options=python.BaseOptions(model_asset_path=model_PATH),
            output_face_blendshapes=True,
            output_facial_transformation_matrixes=True,
            running_mode=vision.RunningMode.LIVE_STREAM,
            result_callback=self.return_result)

        self.detector = vision.FaceLandmarker.create_from_options(options)

    # Create a face detector instance with the live stream mode:
    def return_result(self, result: vision.FaceLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
        self.detection_result = result
        self.output_image = output_image

    def detect(self, image, ts=None):
        self.detector.detect_async(image, ts)
        return self.detection_result



import os
import pygame as pg

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")

def load_image(name, colorkey=None, scale=1):
    fullname = os.path.join(data_dir, name)
    image = pg.image.load(fullname)
    image = image.convert()

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()

class HelmetBody(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = load_image("helmet.png", -1, 1)
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 0, 0


def main():
    
    ##### Pygame Setup #####
    
    pg.init()
    screen = pg.display.set_mode((800, 600), pg.SCALED)
    pg.display.set_caption("Captain Vee")

    # Create The Background
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 177, 64))

    # Display The Background
    screen.blit(background, (0, 0))
    pg.display.flip()

    helmet = HelmetBody()
    allsprites = pg.sprite.RenderPlain((helmet))
    clock = pg.time.Clock()


    ##### Face Landmark Setup #####

    detector = FaceDecector()

    vid = cv2.VideoCapture(0)


    going = True
    while going:
        clock.tick(60)


        ##### Handle Face Landmark Updates #####

        ret, frame = vid.read() 

        if not ret:
            break

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

        frame_timestamp_ms = int(vid.get(cv2.CAP_PROP_POS_MSEC))

        detection_result = detector.detect(mp_image, frame_timestamp_ms)

        jaw_open = False

        if type(detection_result) is not type(None):
            face_landmarks_list = detection_result.face_landmarks

            # Loop through the detected faces to visualize.
            for idx in range(len(face_landmarks_list)):
                face_landmarks = face_landmarks_list[idx]

                talking_val = face_landmarks[15].y - face_landmarks[11].y

                # print(talking_val)

                # print(face_landmarks[11].y - face_landmarks[15].y > 0.012)

                if talking_val > 0.026:
                    jaw_open = True
                    print("open")
                else: 
                    jaw_open = False
            # print(detection_result.facial_transformation_matrixes)
            # jaw_open = detection_result.face_blendshapes[0][25].score


            # image_copy = np.copy(mp_image.numpy_view())
            # annotated_image = draw_landmarks_on_image(image_copy, detection_result)
            # cv2.imshow('frame', cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))


        ##### Handle Pygame Updates #####

        # Handle Input Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                going = False

        # Draw Everything
        screen.blit(background, (0, 0))

        pg.draw.circle(screen, (0,0,0), (200,200),jaw_open * 100)

        # allsprites.draw(screen)
        pg.display.flip()

    pg.quit()
    vid.release() 

if __name__ == "__main__":
    main()