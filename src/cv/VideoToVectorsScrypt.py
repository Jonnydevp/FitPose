import cv2
import mediapipe as mp
import json
import csv
import math
import numpy as np
from tqdm import tqdm


def calculate_angle(a, b, c):
    """Вычисляет угол между тремя точками в градусах (2D проекция)"""
    a = np.array([a.x, a.y])
    b = np.array([b.x, b.y])
    c = np.array([c.x, c.y])

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)
    return np.degrees(angle)


def process_single_side_video(video_path, output_prefix, side='left'):
    # Инициализация MediaPipe
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(
        static_image_mode=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    # Открываем видео
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Ошибка открытия видео: {video_path}")
        return

    # Получаем параметры видео
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Подготовка структур данных
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

    # Обработка кадров с прогресс-баром
    for frame_id in tqdm(range(frame_count), desc=f"Обработка {video_path}"):
        ret, frame = cap.read()
        if not ret:
            break

        # Конвертация и обработка кадра
        results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            side_prefix = side.upper()  # LEFT или RIGHT

            # Получаем нужные точки для одной стороны
            shoulder = getattr(mp_pose.PoseLandmark, f"{side_prefix}_SHOULDER")
            elbow = getattr(mp_pose.PoseLandmark, f"{side_prefix}_ELBOW")
            wrist = getattr(mp_pose.PoseLandmark, f"{side_prefix}_WRIST")
            hip = getattr(mp_pose.PoseLandmark, f"{side_prefix}_HIP")
            knee = getattr(mp_pose.PoseLandmark, f"{side_prefix}_KNEE")
            ankle = getattr(mp_pose.PoseLandmark, f"{side_prefix}_ANKLE")

            # Вычисляем ключевые углы
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

            # Вычисляем скорость (если есть предыдущие данные)
            velocity = 0.0
            if prev_landmarks:
                wrist_pos = np.array([landmarks[wrist].x, landmarks[wrist].y])
                prev_wrist_pos = np.array([prev_landmarks[wrist].x, prev_landmarks[wrist].y])
                velocity = np.linalg.norm(wrist_pos - prev_wrist_pos) * fps

            # Сохраняем в JSON
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

            # Сохраняем в CSV
            csv_rows.append([
                frame_id,
                frame_id / fps,
                elbow_angle,
                knee_angle,
                velocity
            ])

            prev_landmarks = landmarks

    # Закрываем ресурсы
    cap.release()
    pose.close()

    # Сохраняем JSON
    json_path = f"{output_prefix}.json"
    with open(json_path, 'w') as f:
        json.dump(json_data, f, indent=2)

    # Сохраняем CSV
    csv_path = f"{output_prefix}.csv"
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["frame_id", "time_sec", "elbow_angle", "knee_angle", "velocity"])
        writer.writerows(csv_rows)

    print(f"Данные сохранены в {json_path} и {csv_path}")


# Пример использования
if __name__ == "__main__":
    video_path = r"C:\Users\hehe\FitPose\src\cv\video_datasets\10.mp4"  # Укажите путь к видео
    output_prefix = "output_data"  # Префикс для выходных файлов

    # Автоматическое определение стороны по имени файла
    side = 'left'  # Или можно автоматизировать определение

    process_single_side_video(video_path, output_prefix, side)