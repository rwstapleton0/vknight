
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
        connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp.solutions.drawing_styles
        .get_default_face_mesh_tesselation_style())
    # solutions.drawing_utils.draw_landmarks(
    #     image=annotated_image,
    #     landmark_list=face_landmarks_proto,
    #     connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
    #     landmark_drawing_spec=None,
    #     connection_drawing_spec=mp.solutions.drawing_styles
    #     .get_default_face_mesh_contours_style())
    # solutions.drawing_utils.draw_landmarks(
    #     image=annotated_image,
    #     landmark_list=face_landmarks_proto,
    #     connections=mp.solutions.face_mesh.FACEMESH_IRISES,
    #       landmark_drawing_spec=None,
    #       connection_drawing_spec=mp.solutions.drawing_styles
    #       .get_default_face_mesh_iris_connections_style())

  return annotated_image

def plot_face_blendshapes_bar_graph(face_blendshapes):
  # Extract the face blendshapes category names and scores.
  face_blendshapes_names = [face_blendshapes_category.category_name for face_blendshapes_category in face_blendshapes]
  face_blendshapes_scores = [face_blendshapes_category.score for face_blendshapes_category in face_blendshapes]
  # The blendshapes are ordered in decreasing score value.
  face_blendshapes_ranks = range(len(face_blendshapes_names))

  fig, ax = plt.subplots(figsize=(12, 12))
  bar = ax.barh(face_blendshapes_ranks, face_blendshapes_scores, label=[str(x) for x in face_blendshapes_ranks])
  ax.set_yticks(face_blendshapes_ranks, face_blendshapes_names)
  ax.invert_yaxis()

  # Label each bar with values
  for score, patch in zip(face_blendshapes_scores, bar.patches):
    plt.text(patch.get_x() + patch.get_width(), patch.get_y(), f"{score:.4f}", va="top")

  ax.set_xlabel('Score')
  ax.set_title("Face Blendshapes")
  plt.tight_layout()
  plt.show()




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


detector = FaceDecector()

vid = cv2.VideoCapture(0)

while(True):

    ret, frame = vid.read() 

    if not ret:
        break

    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

    frame_timestamp_ms = int(vid.get(cv2.CAP_PROP_POS_MSEC))

    detection_result = detector.detect(mp_image, frame_timestamp_ms)

    if type(detection_result) is not type(None):
      face_landmarks_list = detection_result.face_landmarks

      # Loop through the detected faces to visualize.
      for idx in range(len(face_landmarks_list)):
        face_landmarks = face_landmarks_list[idx]

        talking_val = face_landmarks[15].y - face_landmarks[11].y

        # print(talking_val)

        # print(face_landmarks[11].y - face_landmarks[15].y > 0.012)

        if talking_val > 0.026:
          print("open")


      # Loop through the detected faces to visualize.
      # for idx in range(len(face_landmarks_list)):
      #   face_landmarks = face_landmarks_list[idx]

      # for 
        # print(face_landmarks)
        image_copy = np.copy(mp_image.numpy_view())

        annotated_image = draw_landmarks_on_image(image_copy, detection_result)
        cv2.imshow('frame', cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))

        # plot_face_blendshapes_bar_graph(detection_result.face_blendshapes[0])

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release() 
cv2.destroyAllWindows() 
