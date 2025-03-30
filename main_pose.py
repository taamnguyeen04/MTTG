import cv2
import mediapipe as mp
from pose import is_sitting_straight, estimate_eye_to_screen_distance, extract_pose_landmarks, draw_landmarks_on_image
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Khởi tạo mô hình PoseLandmarker
base_options = python.BaseOptions(model_asset_path='pose_landmarker_heavy.task')
options = vision.PoseLandmarkerOptions(base_options=base_options, output_segmentation_masks=True)
detector = vision.PoseLandmarker.create_from_options(options)

focal_length = 500  # Giả định tiêu cự camera
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Không thể lấy khung hình từ camera. Thoát...")
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    image_height, image_width, _ = frame.shape

    # Nhận diện tư thế
    detection_result = detector.detect(mp_image)
    landmarks = extract_pose_landmarks(detection_result)

    if landmarks:
        left_shoulder, right_shoulder, left_eye, right_eye = landmarks
        eye_distance = estimate_eye_to_screen_distance(left_eye, right_eye, focal_length, image_width)
        straight_status = is_sitting_straight(left_shoulder, right_shoulder)
        annotated_frame = draw_landmarks_on_image(frame, detection_result, eye_distance, straight_status)
    else:
        annotated_frame = frame

    cv2.imshow('Pose Detection', annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
