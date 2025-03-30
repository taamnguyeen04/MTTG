import cv2
import numpy as np
import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


def is_sitting_straight(left_shoulder, right_shoulder, threshold=0.05):
    """
    Kiểm tra tư thế ngồi thẳng dựa vào độ chênh lệch giữa hai vai.
    """
    return abs(left_shoulder.y - right_shoulder.y) < threshold


def estimate_eye_to_screen_distance(left_eye, right_eye, focal_length, image_width, eye_distance_cm=6.3):
    """
    Tính toán khoảng cách từ mắt đến màn hình dựa vào khoảng cách giữa hai mắt.
    """
    x1, x2 = left_eye.x * image_width, right_eye.x * image_width
    y1, y2 = left_eye.y * image_width, right_eye.y * image_width

    eye_distance_pixels = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    if eye_distance_pixels <= 0:
        return None
    return (eye_distance_cm * focal_length) / eye_distance_pixels


def extract_pose_landmarks(detection_result):
    """
    Trích xuất các tọa độ chính từ kết quả phát hiện tư thế.
    """
    if not detection_result.pose_landmarks:
        return None
    pose_landmarks = detection_result.pose_landmarks[0]
    return (
        pose_landmarks[11], pose_landmarks[12],  # Vai trái, Vai phải
        pose_landmarks[2], pose_landmarks[5]  # Mắt trái, Mắt phải
    )


def draw_landmarks_on_image(rgb_image, detection_result, eye_distance, is_straight):
    """
    Vẽ các landmarks lên ảnh và hiển thị thông tin.
    """
    annotated_image = np.copy(rgb_image)
    if not detection_result.pose_landmarks:
        return annotated_image

    text_color = (0, 255, 0) if is_straight else (0, 0, 255)
    status_text = "Sitting straight" if is_straight else "Warning: Not sitting straight!"
    cv2.putText(annotated_image, status_text, (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2, cv2.LINE_AA)

    if eye_distance:
        cv2.putText(annotated_image, f"Distance: {eye_distance:.2f} cm", (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

    # Vẽ landmarks
    pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    pose_landmarks_proto.landmark.extend([
        landmark_pb2.NormalizedLandmark(x=lm.x, y=lm.y, z=lm.z)
        for lm in detection_result.pose_landmarks[0]
    ])
    solutions.drawing_utils.draw_landmarks(
        annotated_image,
        pose_landmarks_proto,
        solutions.pose.POSE_CONNECTIONS,
        solutions.drawing_styles.get_default_pose_landmarks_style()
    )
    return annotated_image


if __name__ == '__main__':
    base_options = python.BaseOptions(model_asset_path='pose_landmarker_heavy.task')
    options = vision.PoseLandmarkerOptions(base_options=base_options, output_segmentation_masks=True)
    detector = vision.PoseLandmarker.create_from_options(options)

    focal_length = 500  # Tiêu cự camera giả định
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Không thể lấy khung hình từ camera. Thoát...")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        image_height, image_width, _ = frame.shape

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
