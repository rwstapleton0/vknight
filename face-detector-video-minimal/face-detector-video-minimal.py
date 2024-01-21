
from typing import Tuple, Union
import math
import cv2
import numpy as np

MARGIN = 10  # pixels
ROW_SIZE = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
TEXT_COLOR = (255, 0, 0)  # red


def _normalized_to_pixel_coordinates(
    normalized_x: float, normalized_y: float, image_width: int,
    image_height: int) -> Union[None, Tuple[int, int]]:
  """Converts normalized value pair to pixel coordinates."""

  # Checks if the float value is between 0 and 1.
  def is_valid_normalized_value(value: float) -> bool:
    return (value > 0 or math.isclose(0, value)) and (value < 1 or
                                                      math.isclose(1, value))

  if not (is_valid_normalized_value(normalized_x) and
          is_valid_normalized_value(normalized_y)):
    # TODO: Draw coordinates even if it's outside of the image bounds.
    return None
  x_px = min(math.floor(normalized_x * image_width), image_width - 1)
  y_px = min(math.floor(normalized_y * image_height), image_height - 1)
  return x_px, y_px


def visualize(
    image,
    detection_result
) -> np.ndarray:
  """Draws bounding boxes and keypoints on the input image and return it.
  Args:
    image: The input RGB image.
    detection_result: The list of all "Detection" entities to be visualize.
  Returns:
    Image with bounding boxes.
  """
  annotated_image = image.copy()
  height, width, _ = image.shape

  for detection in detection_result.detections:
    # Draw bounding_box
    bbox = detection.bounding_box
    start_point = bbox.origin_x, bbox.origin_y
    end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
    cv2.rectangle(annotated_image, start_point, end_point, TEXT_COLOR, 3)

    # Draw keypoints
    for keypoint in detection.keypoints:
      keypoint_px = _normalized_to_pixel_coordinates(keypoint.x, keypoint.y,
                                                     width, height)
      color, thickness, radius = (0, 255, 0), 2, 2
      cv2.circle(annotated_image, keypoint_px, thickness, color, radius)

  return annotated_image

  # STEP 1: Import the necessary modules.
import numpy as np
import mediapipe as mp
import cv2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class FaceDecector:
    detection_result = None
    def __init__(self):
        model_PATH = '/home/yebooty/Programs/mediapipe/face-detector/detector.tflite'

        options = vision.FaceDetectorOptions(
            base_options=python.BaseOptions(model_asset_path=model_PATH),
            running_mode=vision.RunningMode.LIVE_STREAM,
            result_callback=self.return_result)

        self.detector = vision.FaceDetector.create_from_options(options)

    # Create a face detector instance with the live stream mode:
    def return_result(self, result: vision.FaceDetectorResult, output_image: mp.Image, timestamp_ms: int):
        self.detection_result = result

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
        image_copy = np.copy(mp_image.numpy_view())
        annotated_image = visualize(image_copy, detector.detection_result)
        rgb_annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
        cv2.imshow('Frame', rgb_annotated_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release() 
cv2.destroyAllWindows() 
