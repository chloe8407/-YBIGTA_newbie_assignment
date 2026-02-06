"""Ingest embeddings into Pinecone vector index.

Batch upsert: 100 vectors per call.
Metadata: text truncated to 1000 chars (40KB limit).
"""

import json
import os
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from pinecone import Pinecone
from tqdm import tqdm

load_dotenv()

RAW_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "processed"

BATCH_SIZE = 100
TEXT_LIMIT = 1000  # metadata text truncation


def ingest(progress_callback=None):
    """Batch upsert embeddings into Pinecone vector index.

    Args:
        progress_callback: Optional callback(current, total) for progress updates.

    Returns:
        int: Number of vectors upserted.

    Hints:
        - Load embeddings from PROCESSED_DIR / "embeddings.npy"
        - Load IDs from PROCESSED_DIR / "embedding_ids.json"
        - Load texts from RAW_DIR / "corpus.jsonl" for metadata
        - Connect: Pinecone(api_key=...) → pc.Index(index_name)
        - Upsert format: {"id": ..., "values": [...], "metadata": {"text": ...}}
        - Batch size: BATCH_SIZE (100), truncate text to TEXT_LIMIT (1000) chars
    """
    embeddings = np.load(PROCESSED_DIR / "embeddings.npy")
    ids = json.loads((PROCESSED_DIR / "embedding_ids.json").read_text())

    id_to_text = {}
    with open(RAW_DIR / "corpus.jsonl", encoding="utf-8") as f:
        for line in f:
            doc = json.loads(line)
            id_to_text[doc["id"]] = doc["text"]

    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index_name = os.getenv("PINECONE_INDEX", "ragsession")
    index = pc.Index(index_name)

    total_count = 0
    batches = []

    for i in range(0, len(ids), BATCH_SIZE):
        batch_ids = ids[i:i + BATCH_SIZE]
        batch_embeddings = embeddings[i:i + BATCH_SIZE]

        vectors = []
        for doc_id, embedding in zip(batch_ids, batch_embeddings):
            text = id_to_text.get(doc_id, "")
            truncated_text = text[:TEXT_LIMIT]
            vectors.append({
                "id": doc_id,
                "values": embedding.tolist(),
                "metadata": {"text": truncated_text}
            })

        index.upsert(vectors=vectors)
        total_count += len(vectors)

        if progress_callback:
            progress_callback(i // BATCH_SIZE + 1, (len(ids) + BATCH_SIZE - 1) // BATCH_SIZE)

    return total_count


if __name__ == "__main__":
    ingest()
