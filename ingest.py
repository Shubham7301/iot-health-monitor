
import os
from parser import parse_file
from embedder import ingest, get_stats

CSV_FILES = {
    "patients": "./iot_data/patients.csv",
    "heart_rate": "./iot_data/heart_rate.csv",
    "spo2": "./iot_data/spo2.csv",
    "temperature": "./iot_data/temperature.csv",
    "blood_pressure": "./iot_data/blood_pressure.csv",
    "activity": "./iot_data/activity.csv",
}

for source, path in CSV_FILES.items():
    if not os.path.exists(path):
        print(f"Missing: {path}")
        continue

    print(f"Ingesting {source}...")
    text = parse_file(path, source)
    count = ingest(text, source, os.path.basename(path), source)
    print(f"{source}: {count} chunks stored")

print(get_stats())
