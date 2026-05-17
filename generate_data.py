
import os
import random
from faker import Faker
import pandas as pd
from datetime import datetime, timedelta

fake = Faker("en_IN")
random.seed(42)
Faker.seed(42)

os.makedirs("iot_data", exist_ok=True)

PATIENTS = 5

conditions = [
    "None", "None", "Hypertension",
    "Type 2 Diabetes", "Asthma", "COPD"
]

wards = [
    "General", "ICU", "Cardiology",
    "Pulmonology", "Neurology"
]

start = datetime(2024, 1, 15, 0, 0, 0)

def risk_score(age, condition, smoker, bmi):
    score = 0
    if age > 60:
        score += 2
    if condition != "None":
        score += 2
    if smoker == "Yes":
        score += 1
    if bmi > 30:
        score += 1
    return min(score, 5)

patients = []
for i in range(1, PATIENTS + 1):
    pid = f"P{i:04d}"
    age = random.randint(25, 85)
    weight = round(random.uniform(50, 95), 1)
    height = round(random.uniform(150, 185), 1)
    bmi = round(weight / ((height / 100) ** 2), 1)
    condition = random.choice(conditions)
    smoker = random.choice(["Yes", "No", "Former"])

    patients.append({
        "patient_id": pid,
        "name": fake.name(),
        "age": age,
        "sex": random.choice(["Male", "Female"]),
        "date_of_birth": fake.date_of_birth(minimum_age=age, maximum_age=age),
        "blood_group": random.choice(["A+", "B+", "O+", "AB+"]),
        "weight_kg": weight,
        "height_cm": height,
        "bmi": bmi,
        "city": fake.city(),
        "state": fake.state(),
        "contact_number": fake.phone_number(),
        "emergency_contact": fake.phone_number(),
        "admitted_on": "2024-01-15",
        "ward": random.choice(wards),
        "bed_number": f"B{i:03d}",
        "doctor_assigned": "Dr. Sharma",
        "known_condition": condition,
        "allergies": random.choice(["None", "Dust", "Pollen"]),
        "smoker": smoker,
        "alcohol": random.choice(["Yes", "No"]),
    })

patients_df = pd.DataFrame(patients)
patients_df.to_csv("iot_data/patients.csv", index=False)

heart_rows = []
spo2_rows = []
temp_rows = []
bp_rows = []
activity_rows = []

for p in patients:
    rs = risk_score(p["age"], p["known_condition"], p["smoker"], p["bmi"])

    for j in range(60):
        ts = start + timedelta(seconds=30*j)
        bpm = random.randint(65+rs*2, 90+rs*4)
        irregular = random.random() < (0.05 * rs)
        heart_rows.append({
            "patient_id": p["patient_id"],
            "timestamp": ts,
            "bpm": bpm,
            "irregular_flag": irregular,
            "activity_state": random.choice(["resting", "walking", "sleeping"])
        })

    for j in range(30):
        ts = start + timedelta(minutes=j)
        base_spo2 = 97 if p["known_condition"] in ["COPD", "Asthma"] else 98.5
        spo2 = round(random.uniform(base_spo2-3, base_spo2),1)
        spo2_rows.append({
            "patient_id": p["patient_id"],
            "timestamp": ts,
            "spo2_pct": spo2,
            "perfusion_index": round(random.uniform(1.0,3.0),1),
            "low_oxygen_flag": spo2 < 92
        })

    for j in range(12):
        ts = start + timedelta(minutes=5*j)
        temp = round(random.uniform(36.2,39.5),1)
        temp_rows.append({
            "patient_id": p["patient_id"],
            "timestamp": ts,
            "temp_celsius": temp,
            "temp_fahrenheit": round((temp*9/5)+32,1),
            "fever_flag": temp > 38,
            "hypothermia_flag": temp < 35
        })

    for j in range(6):
        ts = start + timedelta(minutes=15*j)
        sys = random.randint(110,130)
        if p["known_condition"] == "Hypertension":
            sys += 20
        dia = random.randint(70,95)
        bp_rows.append({
            "patient_id": p["patient_id"],
            "timestamp": ts,
            "systolic": sys,
            "diastolic": dia,
            "pulse_pressure": sys-dia,
            "hypertension_flag": sys > 140,
            "hypotension_flag": sys < 90
        })

    for j in range(10):
        ts = start + timedelta(minutes=10*j)
        fall = random.random() < (0.2 if p["age"] > 70 else 0.05)
        activity_rows.append({
            "patient_id": p["patient_id"],
            "timestamp": ts,
            "steps_count": random.randint(0,500),
            "activity_level": random.choice(["sedentary","walking","active"]),
            "sleep_stage": random.choice(["light","deep","awake"]),
            "calories_burned": round(random.uniform(1,20),1),
            "fall_detected": fall
        })

pd.DataFrame(heart_rows).to_csv("iot_data/heart_rate.csv", index=False)
pd.DataFrame(spo2_rows).to_csv("iot_data/spo2.csv", index=False)
pd.DataFrame(temp_rows).to_csv("iot_data/temperature.csv", index=False)
pd.DataFrame(bp_rows).to_csv("iot_data/blood_pressure.csv", index=False)
pd.DataFrame(activity_rows).to_csv("iot_data/activity.csv", index=False)

print("Dummy IoT healthcare data generated successfully.")
