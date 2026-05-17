
# IoT Patient Health Monitoring Chatbot

RAG-powered IoT healthcare chatbot using FastAPI, ChromaDB, OpenAI, and React.

## Run

```bash
pip install -r requirements.txt
cp .env.example .env
python generate_data.py
python ingest.py
uvicorn main:app --reload --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm start
```
