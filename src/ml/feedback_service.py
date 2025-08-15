import requests
import json
import os
import pandas as pd
from scipy.signal import find_peaks
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("API key not found")


def analyze_workout_data(df):
    # find peaks and troughs
    peaks, _ = find_peaks(-df['elbow_angle'], height=-100, distance=30)
    troughs, _ = find_peaks(df['elbow_angle'], height=160, distance=30)

    rep_count = min(len(peaks), len(troughs))

    if rep_count == 0:
        return None
    
    min_elbow_angles = [df['elbow_angle'][p] for p in peaks[:rep_count]]
    max_elbow_angles = [df['elbow_angle'][t] for t in troughs[:rep_count]]
    
    peak_velocities_concentric = []
    peak_velocities_eccentric = []
    
    for i in range(rep_count):
        start_frame = troughs[i]
        mid_frame = peaks[i]

        end_frame = troughs[i+1] if i + 1 < len(troughs) else len(df) - 1

        concentric_phase = df.iloc[start_frame:mid_frame]
        if not concentric_phase.empty:
            peak_velocities_concentric.append(concentric_phase['velocity'].max())

        eccentric_phase = df.iloc[mid_frame:end_frame]
        if not eccentric_phase.empty:
            peak_velocities_eccentric.append(eccentric_phase['velocity'].max())

    metrics = {
        "rep_count": rep_count,
        "min_elbow_angle_avg": sum(min_elbow_angles) / len(min_elbow_angles) if min_elbow_angles else 0,
        "max_elbow_angle_avg": sum(max_elbow_angles) / len(max_elbow_angles) if max_elbow_angles else 0,
        "knee_angle_range": df['knee_angle'].max() - df['knee_angle'].min(),
        "avg_peak_velocity_concentric": sum(peak_velocities_concentric) / len(peak_velocities_concentric) if peak_velocities_concentric else 0,
        "avg_peak_velocity_eccentric": sum(peak_velocities_eccentric) / len(peak_velocities_eccentric) if peak_velocities_eccentric else 0,
    }
    return metrics



try:
    user_data_df = pd.read_csv("output_data.csv")
    stats = analyze_workout_data(user_data_df)

except FileNotFoundError:
    print("Error: file not found")
    exit()

if not stats:
    print("Unable to analyze video")
    exit()

prompt_template = f"""
Ты — опытный фитнес-тренер и эксперт по биомеханике. Твоя задача — проанализировать данные о выполнении упражнения "подъем на бицепс", снятого сбоку. Данные представлены в виде временного ряда с углами в локтевом и коленном суставах, а также скоростью движения запястья.

# Правила анализа техники подъема на бицепс:
1.  **Фаза подъема (Концентрическая):** Угол в локте (`elbow_angle`) плавно уменьшается с ~175-180 градусов до ~30-50 градусов.
2.  **Фаза опускания (Эксцентрическая):** Угол в локте (`elbow_angle`) плавно увеличивается обратно до ~175-180 градусов. Эта фаза должна быть контролируемой.
3.  **Стабильность корпуса:** Угол в колене (`knee_angle`) должен оставаться практически неизменным (170-180 градусов). Значительные изменения (более 7-10 градусов) указывают на читинг.
4.  **Плавность движения:** Скорость (`velocity`) должна плавно нарастать и убывать. Резкие пики скорости указывают на рывковое движение.

# Распространенные ошибки:
- **Читинг:** Если `knee_angle` значительно проседает.
- **Неполная амплитуда:** Если минимальный `elbow_angle` > 65 градусов, ИЛИ максимальный `elbow_angle` < 165 градусов.
- **Рывковое движение:** Если есть аномально высокие пики `velocity`.
- **Слишком быстрое опускание:** Если скорость на фазе опускания значительно выше, чем на фазе подъема.

# Задача:
Проанализируй предоставленные ниже данные одного подхода. На основе этих данных и правил, дай краткий и четкий текстовый отчет.

**Формат ответа (строго придерживайся этого формата):**
- Общая оценка: [Одно предложение]
- Ошибки: [Перечислить через запятую, или "Не обнаружены"]
- Рекомендации: [Краткие советы в виде маркированного списка]

# Данные для анализа:
- Количество полных повторений: {stats['rep_count']}
- Средний минимальный угол локтя (пик сгибания): {stats['min_elbow_angle_avg']:.1f} градусов
- Средний максимальный угол локтя (в нижней точке): {stats['max_elbow_angle_avg']:.1f} градусов
- Максимальное изменение угла в колене за подход: {stats['knee_angle_range']:.1f} градусов
- Средняя пиковая скорость на подъеме: {stats['avg_peak_velocity_concentric']:.2f}
- Средняя пиковая скорость на опускании: {stats['avg_peak_velocity_eccentric']:.2f}

# Твой анализ:
"""

try:

    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    data=json.dumps({
        "model": "openai/gpt-oss-20b:free",
        "messages": [
        {
            "role": "user",
            "content": prompt_template
        }
        ],
        
    })
    )

    if response.status_code == 200:
        response_json = response.json()
        model_reply =  response_json['choices'][0]['message']['content']
        print("Answer")
        print(model_reply)

    else:
        print("Error!")
        print(f"Error text: {response.text}")


except requests.exceptions.RequestException as e:
    print(f"Error sending request: {e}")