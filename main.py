from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from searcher import search
from embedder import get_stats

import pandas as pd
import math

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str


# =========================
# LOAD CSV FILES
# =========================

PATIENTS = pd.read_csv(
    "iot_data/patients.csv"
).fillna("")

HEART = pd.read_csv(
    "iot_data/heart_rate.csv"
).fillna("")

SPO2 = pd.read_csv(
    "iot_data/spo2.csv"
).fillna("")

TEMP = pd.read_csv(
    "iot_data/temperature.csv"
).fillna("")

BP = pd.read_csv(
    "iot_data/blood_pressure.csv"
).fillna("")

ACTIVITY = pd.read_csv(
    "iot_data/activity.csv"
).fillna("")


# =========================
# CLEAN NaN VALUES
# =========================

def clean_nan(obj):

    if isinstance(obj, dict):

        return {
            k: clean_nan(v)
            for k, v in obj.items()
        }

    elif isinstance(obj, list):

        return [clean_nan(x) for x in obj]

    elif isinstance(obj, float):

        if math.isnan(obj):
            return None

    return obj


# =========================
# HEALTH ENDPOINT
# =========================

@app.get("/health")
def health():

    return {
        "status": "ok",
        "message": "IoT Health Chatbot is running."
    }


# =========================
# STATS ENDPOINT
# =========================

@app.get("/stats")
def stats():

    return {
        **get_stats(),
        "patients": len(PATIENTS),
        "sensor_types": 5
    }


# =========================
# GET ALL PATIENTS
# =========================

@app.get("/patients")
def get_patients():

    response = PATIENTS.to_dict(orient="records")

    return clean_nan(response)


# =========================
# PATIENT DASHBOARD
# =========================

@app.get("/patient/{patient_id}")
def patient_dashboard(patient_id: str):

    patient = PATIENTS[
        PATIENTS["patient_id"] == patient_id
    ]

    if patient.empty:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    patient = patient.iloc[0].to_dict()

    heart = HEART[
        HEART["patient_id"] == patient_id
    ]

    spo2 = SPO2[
        SPO2["patient_id"] == patient_id
    ]

    temp = TEMP[
        TEMP["patient_id"] == patient_id
    ]

    bp = BP[
        BP["patient_id"] == patient_id
    ]

    activity = ACTIVITY[
        ACTIVITY["patient_id"] == patient_id
    ]

    latest_heart = heart.iloc[-1].to_dict()
    latest_spo2 = spo2.iloc[-1].to_dict()
    latest_temp = temp.iloc[-1].to_dict()
    latest_bp = bp.iloc[-1].to_dict()
    latest_activity = activity.iloc[-1].to_dict()

    alerts = []

    if latest_temp["fever_flag"]:
        alerts.append("FEVER DETECTED")

    if latest_spo2["low_oxygen_flag"]:
        alerts.append("LOW OXYGEN ALERT")

    if latest_bp["hypertension_flag"]:
        alerts.append("HYPERTENSION ALERT")

    if latest_activity["fall_detected"]:
        alerts.append("FALL DETECTED")

    response = {

        "patient": patient,

        "summary": {

            "heart_rate": latest_heart,

            "spo2": latest_spo2,

            "temperature": latest_temp,

            "blood_pressure": latest_bp,

            "activity": latest_activity,

            "alerts": alerts
        },

        "charts": {

            "heart_rate": heart[
                ["timestamp", "bpm"]
            ].tail(20).to_dict(orient="records"),

            "spo2": spo2[
                ["timestamp", "spo2_pct"]
            ].tail(20).to_dict(orient="records"),

            "temperature": temp[
                ["timestamp", "temp_celsius"]
            ].tail(20).to_dict(orient="records")
        }
    }

    return clean_nan(response)


# =========================
# CHAT ENDPOINT
# =========================

@app.post("/chat")
def chat(req: ChatRequest):

    if not req.query.strip():

        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty"
        )

    return search(req.query)