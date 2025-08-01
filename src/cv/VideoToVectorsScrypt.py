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

if __name__ == "__main__":
    output_prefix = "output_data"
    side = 'left'
    base_dir = "your path"
    all_json_frames = []
    all_csv_rows = []
    global_frame_id = 0

    for i in range(15):
        video_path = base_dir + "\\" + str(i) + ".mp4"

        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose(
            static_image_mode=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error opening video: {video_path}")
            continue

        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        prev_landmarks = None

        for frame_id in tqdm(range(frame_count), desc=f"Processing {video_path}"):
            ret, frame = cap.read()
            if not ret:
                break

            results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                side_prefix = side.upper()

                shoulder = getattr(mp_pose.PoseLandmark, f"{side_prefix}_SHOULDER")
                elbow = getattr(mp_pose.PoseLandmark, f"{side_prefix}_ELBOW")
                wrist = getattr(mp_pose.PoseLandmark, f"{side_prefix}_WRIST")
                hip = getattr(mp_pose.PoseLandmark, f"{side_prefix}_HIP")
                knee = getattr(mp_pose.PoseLandmark, f"{side_prefix}_KNEE")
                ankle = getattr(mp_pose.PoseLandmark, f"{side_prefix}_ANKLE")

                elbow_angle = calculate_angle(landmarks[shoulder], landmarks[elbow], landmarks[wrist])
                knee_angle = calculate_angle(landmarks[hip], landmarks[knee], landmarks[ankle])

                velocity = 0.0
                if prev_landmarks:
                    wrist_pos = np.array([landmarks[wrist].x, landmarks[wrist].y])
                    prev_wrist_pos = np.array([prev_landmarks[wrist].x, prev_landmarks[wrist].y])
                    velocity = np.linalg.norm(wrist_pos - prev_wrist_pos) * fps

                frame_data = {
                    "frame_id": global_frame_id,
                    "time_sec": global_frame_id / fps,
                    "video": f"{i}.mp4",
                    "angles": {
                        "elbow": elbow_angle,
                        "knee": knee_angle
                    },
                    "velocity": velocity
                }
                all_json_frames.append(frame_data)

                all_csv_rows.append([
                    global_frame_id,
                    global_frame_id / fps,
                    f"{i}.mp4",
                    elbow_angle,
                    knee_angle,
                    velocity
                ])

                prev_landmarks = landmarks
                global_frame_id += 1

        cap.release()
        pose.close()

    with open(f"{output_prefix}.json", 'w') as f_json:
        json.dump({"frames": all_json_frames}, f_json, indent=2)

    with open(f"{output_prefix}.csv", 'w', newline='') as f_csv:
        writer = csv.writer(f_csv)
        writer.writerow(["frame_id", "time_sec", "video", "elbow_angle", "knee_angle", "velocity"])
        writer.writerows(all_csv_rows)
