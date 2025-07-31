import cv2
import mediapipe as mp
import json
import csv
import numpy as np
from tqdm import tqdm


def calculate_angle(a, b, c):
    a = np.array([a.x, a.y])
    b = np.array([b.x, b.y])
    c = np.array([c.x, c.y])

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)
    return np.degrees(angle)


def process_single_side_video(video_path, output_prefix, side='left'):
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(
        static_image_mode=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Ошибка открытия видео: {video_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    json_data = {
        "video_info": {
            "filename": video_path.split('/')[-1],
            "resolution": [width, height],
            "fps": fps,
            "side_view": True,
            "tracked_side": side
        },
        "frames": []
    }

    csv_rows = []
    prev_landmarks = None

    for frame_id in tqdm(range(frame_count), desc=f"Обработка {video_path}"):
        ret, frame = cap.read()
        if not ret:
            break

        results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            side_prefix = side.upper()  # LEFT или RIGHT

            shoulder = getattr(mp_pose.PoseLandmark, f"{side_prefix}_SHOULDER")
            elbow = getattr(mp_pose.PoseLandmark, f"{side_prefix}_ELBOW")
            wrist = getattr(mp_pose.PoseLandmark, f"{side_prefix}_WRIST")
            hip = getattr(mp_pose.PoseLandmark, f"{side_prefix}_HIP")
            knee = getattr(mp_pose.PoseLandmark, f"{side_prefix}_KNEE")
            ankle = getattr(mp_pose.PoseLandmark, f"{side_prefix}_ANKLE")

            elbow_angle = calculate_angle(
                landmarks[shoulder],
                landmarks[elbow],
                landmarks[wrist]
            )

            knee_angle = calculate_angle(
                landmarks[hip],
                landmarks[knee],
                landmarks[ankle]
            )

            velocity = 0.0
            if prev_landmarks:
                wrist_pos = np.array([landmarks[wrist].x, landmarks[wrist].y])
                prev_wrist_pos = np.array([prev_landmarks[wrist].x, prev_landmarks[wrist].y])
                velocity = np.linalg.norm(wrist_pos - prev_wrist_pos) * fps

            frame_data = {
                "frame_id": frame_id,
                "time_sec": frame_id / fps,
                "angles": {
                    "elbow": elbow_angle,
                    "knee": knee_angle
                },
                "velocity": velocity
            }
            json_data["frames"].append(frame_data)

            csv_rows.append([
                frame_id,
                frame_id / fps,
                elbow_angle,
                knee_angle,
                velocity
            ])

            prev_landmarks = landmarks

    cap.release()
    pose.close()

    json_path = f"{output_prefix}.json"
    with open(json_path, 'w') as f:
        json.dump(json_data, f, indent=2)

    csv_path = f"{output_prefix}.csv"
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["frame_id", "time_sec", "elbow_angle", "knee_angle", "velocity"])
        writer.writerows(csv_rows)

    print(f"Данные сохранены в {json_path} и {csv_path}")

if __name__ == "__main__":
    video_path = r"C:\Users\hehe\FitPose\src\cv\video_datasets\10.mp4"
    output_prefix = "output_data"

    side = 'left'

    process_single_side_video(video_path, output_prefix, side)