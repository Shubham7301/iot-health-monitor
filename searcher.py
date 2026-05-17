import pandas as pd

from embedder import query
from openai import OpenAI
from config import *

client = OpenAI(api_key=OPENAI_API_KEY)

PATIENTS = pd.read_csv(
    "iot_data/patients.csv"
).fillna("")

SYSTEM_PROMPT = """
You are an IoT-powered patient monitoring assistant.

Rules:
- Answer ONLY using provided context
- Cite sources
- Never hallucinate
- If abnormal vitals exist, mention ALERT
"""

# =========================
# DIRECT PATIENT LOOKUP
# =========================

def patient_lookup(user_query):

    q = user_query.lower()

    for _, row in PATIENTS.iterrows():

        pid = str(row["patient_id"]).lower()
        name = str(row["name"]).lower()

        # AGE QUERY
        if (
            ("age" in q)
            and (pid in q or name in q)
        ):

            return {
                "answer":
                    f"Patient {row['patient_id']} "
                    f"({row['name']}) is "
                    f"{row['age']} years old. "
                    f"[patients.csv]",

                "sources": [
                    {
                        "source": "patients.csv"
                    }
                ],

                "chunks_used": 0
            }

        # NAME QUERY
        if (
            ("name" in q)
            and (pid in q)
        ):

            return {
                "answer":
                    f"The name of "
                    f"{row['patient_id']} is "
                    f"{row['name']}. "
                    f"[patients.csv]",

                "sources": [
                    {
                        "source": "patients.csv"
                    }
                ],

                "chunks_used": 0
            }

        # CONDITION QUERY
        if (
            ("condition" in q or "disease" in q)
            and (pid in q or name in q)
        ):

            return {
                "answer":
                    f"Patient {row['patient_id']} "
                    f"({row['name']}) has "
                    f"{row['known_condition']}. "
                    f"[patients.csv]",

                "sources": [
                    {
                        "source": "patients.csv"
                    }
                ],

                "chunks_used": 0
            }

    return None


# =========================
# MAIN SEARCH
# =========================

def search(user_query):

    # TRY DIRECT LOOKUP FIRST
    direct = patient_lookup(user_query)

    if direct:
        return direct

    # OTHERWISE USE RAG
    chunks = query(
        user_query,
        top_k=TOP_K_RETRIEVE
    )

    if not chunks:

        return {
            "answer":
                "No sensor data found.",
            "sources": [],
            "chunks_used": 0
        }

    chunks = sorted(
        chunks,
        key=lambda x: x["score"],
        reverse=True
    )[:TOP_K_RERANK]

    context = ""

    for i, c in enumerate(chunks, 1):

        context += (
            f"[{i}] "
            f"Source: {c['meta']['source']}\n"
            f"{c['text']}\n\n"
        )

    response = client.chat.completions.create(

        model=CHAT_MODEL,

        messages=[

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },

            {
                "role": "user",
                "content":
                    f"Context:\n{context}\n\n"
                    f"Question: {user_query}"
            }
        ]
    )

    return {

        "answer":
            response.choices[0]
            .message.content,

        "sources": [

            {
                "index": i + 1,
                "source":
                    c["meta"]["source"],
                "score":
                    round(c["score"], 3),
                "excerpt":
                    c["text"][:200]
            }

            for i, c in enumerate(chunks)
        ],

        "chunks_used": len(chunks)
    }