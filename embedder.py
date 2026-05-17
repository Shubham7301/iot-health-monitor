
import chromadb
import tiktoken
from openai import OpenAI
from config import *
import uuid

client = OpenAI(api_key=OPENAI_API_KEY)

chroma = chromadb.PersistentClient(path=CHROMA_PATH)

collection = chroma.get_or_create_collection(
    name="iot_health",
    metadata={"hnsw:space": "cosine"}
)

enc = tiktoken.get_encoding("cl100k_base")

def chunk_text(text):
    tokens = enc.encode(text)
    chunks = []
    step = CHUNK_SIZE - CHUNK_OVERLAP

    for i in range(0, len(tokens), step):
        chunk = enc.decode(tokens[i:i+CHUNK_SIZE])
        chunks.append(chunk)
    return chunks

def embed(texts):
    res = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts
    )
    return [x.embedding for x in res.data]

def ingest(text, source, title, doc_id):
    chunks = chunk_text(text)
    embeds = embed(chunks)

    ids = [str(uuid.uuid4()) for _ in chunks]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeds,
        metadatas=[
            {
                "source": source,
                "title": title,
                "doc_id": doc_id,
                "chunk_index": i
            }
            for i in range(len(chunks))
        ]
    )

    return len(chunks)

def query(query_text, top_k=8):
    emb = embed([query_text])[0]

    res = collection.query(
        query_embeddings=[emb],
        n_results=top_k
    )

    results = []

    for i in range(len(res["documents"][0])):
        results.append({
            "text": res["documents"][0][i],
            "score": 1 - res["distances"][0][i],
            "meta": res["metadatas"][0][i]
        })

    return results

def get_stats():
    return {"total_chunks": collection.count()}
