
import pandas as pd

def parse_patients(filepath):
    df = pd.read_csv(filepath)
    texts = []
    for _, r in df.iterrows():
        texts.append(
            f"Patient {r.patient_id} name: {r.name}, age {r.age}, "
            f"{r.sex}, from {r.city}, {r.state}. "
            f"Known condition: {r.known_condition}. "
            f"BMI: {r.bmi}. Ward: {r.ward}."
        )
    return "\n".join(texts)

def parse_heart_rate(filepath):
    df = pd.read_csv(filepath)
    texts = []
    for _, r in df.iterrows():
        alert = "IRREGULAR RHYTHM DETECTED." if r.irregular_flag else "Normal rhythm."
        texts.append(
            f"Patient {r.patient_id} heart rate: {r.bpm} BPM at {r.timestamp}. "
            f"{alert} Activity state: {r.activity_state}."
        )
    return "\n".join(texts)

def parse_spo2(filepath):
    df = pd.read_csv(filepath)
    texts = []
    for _, r in df.iterrows():
        alert = "LOW OXYGEN ALERT." if r.low_oxygen_flag else ""
        texts.append(
            f"Patient {r.patient_id} blood oxygen (SpO2): {r.spo2_pct}% at {r.timestamp}. "
            f"{alert}"
        )
    return "\n".join(texts)

def parse_temperature(filepath):
    df = pd.read_csv(filepath)
    texts = []
    for _, r in df.iterrows():
        alert = "FEVER DETECTED." if r.fever_flag else ""
        texts.append(
            f"Patient {r.patient_id} body temperature: {r.temp_celsius}°C "
            f"({r.temp_fahrenheit}°F) at {r.timestamp}. {alert}"
        )
    return "\n".join(texts)

def parse_blood_pressure(filepath):
    df = pd.read_csv(filepath)
    texts = []
    for _, r in df.iterrows():
        alert = "HYPERTENSION ALERT." if r.hypertension_flag else ""
        texts.append(
            f"Patient {r.patient_id} blood pressure: "
            f"{r.systolic}/{r.diastolic} mmHg at {r.timestamp}. {alert}"
        )
    return "\n".join(texts)

def parse_activity(filepath):
    df = pd.read_csv(filepath)
    texts = []
    for _, r in df.iterrows():
        alert = "FALL DETECTED." if r.fall_detected else "No fall."
        texts.append(
            f"Patient {r.patient_id} activity: {r.steps_count} steps, "
            f"level {r.activity_level} at {r.timestamp}. {alert}"
        )
    return "\n".join(texts)

def parse_file(filepath, source):
    funcs = {
        "patients": parse_patients,
        "heart_rate": parse_heart_rate,
        "spo2": parse_spo2,
        "temperature": parse_temperature,
        "blood_pressure": parse_blood_pressure,
        "activity": parse_activity
    }
    return funcs[source](filepath)
