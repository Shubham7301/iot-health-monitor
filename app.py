import streamlit as st
import pandas as pd
import plotly.express as px

from searcher import search

# =========================
# PAGE CONFIG
# =========================¯

st.set_page_config(
    page_title="IoT Health Monitor",
    page_icon="🏥",
    layout="wide"
)

# =========================
# LOAD DATA
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
# SIDEBAR
# =========================

st.sidebar.title("🏥 IoT Health Monitor")

patient_options = [
    f"{r.patient_id} - {r.name}"
    for _, r in PATIENTS.iterrows()
]

selected = st.sidebar.selectbox(
    "Select Patient",
    patient_options
)

selected_id = selected.split(" - ")[0]

# =========================
# FILTER DATA
# =========================

patient = PATIENTS[
    PATIENTS["patient_id"] == selected_id
].iloc[0]

heart = HEART[
    HEART["patient_id"] == selected_id
]

spo2 = SPO2[
    SPO2["patient_id"] == selected_id
]

temp = TEMP[
    TEMP["patient_id"] == selected_id
]

bp = BP[
    BP["patient_id"] == selected_id
]

activity = ACTIVITY[
    ACTIVITY["patient_id"] == selected_id
]

latest_heart = heart.iloc[-1]
latest_spo2 = spo2.iloc[-1]
latest_temp = temp.iloc[-1]
latest_bp = bp.iloc[-1]
latest_activity = activity.iloc[-1]

# =========================
# HEADER
# =========================

st.title("🏥 IoT Patient Monitoring Dashboard")

st.markdown(
    "AI + RAG + GPT-4o Healthcare Monitoring System"
)

# =========================
# ALERTS
# =========================

alerts = []

if latest_temp["fever_flag"]:
    alerts.append("🔥 FEVER DETECTED")

if latest_spo2["low_oxygen_flag"]:
    alerts.append("🫁 LOW OXYGEN ALERT")

if latest_bp["hypertension_flag"]:
    alerts.append("❤️ HYPERTENSION ALERT")

if latest_activity["fall_detected"]:
    alerts.append("⚠️ FALL DETECTED")

for a in alerts:
    st.error(a)

# =========================
# PATIENT INFO
# =========================

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric(
        "Patient",
        patient["name"]
    )

with c2:
    st.metric(
        "Heart Rate",
        f"{latest_heart['bpm']} BPM"
    )

with c3:
    st.metric(
        "SpO2",
        f"{latest_spo2['spo2_pct']}%"
    )

with c4:
    st.metric(
        "Temperature",
        f"{latest_temp['temp_celsius']}°C"
    )

with c5:
    st.metric(
        "Blood Pressure",
        f"{latest_bp['systolic']}/{latest_bp['diastolic']}"
    )

# =========================
# PATIENT DETAILS
# =========================

st.subheader("Patient Details")

col1, col2 = st.columns(2)

with col1:
    st.write(f"**Patient ID:** {patient['patient_id']}")
    st.write(f"**Age:** {patient['age']}")
    st.write(f"**Sex:** {patient['sex']}")
    st.write(f"**Blood Group:** {patient['blood_group']}")
    st.write(f"**Condition:** {patient['known_condition']}")

with col2:
    st.write(f"**Ward:** {patient['ward']}")
    st.write(f"**Doctor:** {patient['doctor_assigned']}")
    st.write(f"**BMI:** {patient['bmi']}")
    st.write(f"**Smoker:** {patient['smoker']}")
    st.write(f"**Alcohol:** {patient['alcohol']}")

# =========================
# CHARTS
# =========================

st.subheader("📈 Vital Trends")

chart1, chart2 = st.columns(2)

with chart1:

    fig = px.line(
        heart.tail(30),
        x="timestamp",
        y="bpm",
        title="Heart Rate Trend"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with chart2:

    fig = px.line(
        spo2.tail(30),
        x="timestamp",
        y="spo2_pct",
        title="SpO2 Trend"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

fig = px.line(
    temp.tail(20),
    x="timestamp",
    y="temp_celsius",
    title="Temperature Trend"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================
# AI CHATBOT
# =========================

st.subheader("🤖 AI Healthcare Assistant")

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello 👋\n"
                "Ask me anything about patient vitals, alerts, oxygen levels, heart rate, fever, or risks."
            )
        }
    ]

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input(
    "Ask healthcare question..."
)

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Analyzing sensor data..."):

            result = search(prompt)

            answer = result["answer"]

            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )