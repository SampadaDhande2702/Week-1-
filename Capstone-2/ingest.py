import fitz
import json
import re
import os
import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db")
os.makedirs(DB_PATH, exist_ok=True)

_client = chromadb.PersistentClient(path=DB_PATH)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def get_collection():
    return _client.get_or_create_collection("truth_engine")

def chunk_text(text, chunk_size=60, overlap=10):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def ingest_pdf(filepath):
    print(f"Ingesting PDF: {filepath}")
    try:
        col = get_collection()
        doc = fitz.open(filepath)
        full_text = "".join(page.get_text() for page in doc)
        doc.close()
        chunks = chunk_text(full_text)
        for i, chunk in enumerate(chunks):
            col.add(
                documents=[chunk],
                embeddings=[embedder.encode(chunk).tolist()],
                ids=[f"pdf_{i}"],
                metadatas=[{"source": "A", "source_name": "Technical Manual", "file": filepath, "priority": 1}]
            )
        print(f"  PDF done: {len(chunks)} chunks")
    except Exception as e:
        print(f"  ERROR ingesting PDF: {e}")

def ingest_json(filepath):
    print(f"Ingesting JSON: {filepath}")
    try:
        col = get_collection()
        with open(filepath, "r") as f:
            data = json.load(f)
        for i, item in enumerate(data):
            text = " | ".join(f"{k}: {v}" for k, v in item.items())
            col.add(
                documents=[text],
                embeddings=[embedder.encode(text).tolist()],
                ids=[f"json_{i}"],
                metadatas=[{"source": "B", "source_name": "Support Logs", "file": filepath, "priority": 2}]
            )
        print(f"  JSON done: {len(data)} entries")
    except Exception as e:
        print(f"  ERROR ingesting JSON: {e}")

def ingest_markdown(filepath):
    print(f"Ingesting Markdown: {filepath}")
    try:
        col = get_collection()
        with open(filepath, "r", encoding="utf-8") as f:
            raw = f.read()
        text = re.sub(r'#{1,6}\s*', '', raw)
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
        text = re.sub(r'\*(.*?)\*', r'\1', text)
        text = re.sub(r'`(.*?)`', r'\1', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        chunks = chunk_text(text)
        for i, chunk in enumerate(chunks):
            col.add(
                documents=[chunk],
                embeddings=[embedder.encode(chunk).tolist()],
                ids=[f"md_{i}"],
                metadatas=[{"source": "C", "source_name": "Legacy Wiki", "file": filepath, "priority": 3}]
            )
        print(f"  Markdown done: {len(chunks)} chunks")
    except Exception as e:
        print(f"  ERROR ingesting Markdown: {e}")

if __name__ == "__main__":
    ingest_pdf("data/laptop_manual.pdf")
    ingest_json("data/laptop_sales_logs.json")
    ingest_markdown("data/laptop_wiki.md")
    print(f"\nTotal chunks in DB: {get_collection().count()}")