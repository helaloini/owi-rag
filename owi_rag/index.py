"""docs.jsonl -> chunks.jsonl + BM25 index + FAISS index."""
import json
from pathlib import Path

from .chunk import chunk

MODEL = "intfloat/multilingual-e5-small"


def build(data="data"):
    import bm25s
    import faiss
    from sentence_transformers import SentenceTransformer

    d = Path(data)
    chunks = []
    with open(d / "docs.jsonl", encoding="utf-8") as f:
        for i, line in enumerate(f):
            doc = json.loads(line)
            for j, text in enumerate(chunk(doc["text"])):
                chunks.append({"id": f"{i}-{j}", "url": doc["url"], "text": text})
    with open(d / "chunks.jsonl", "w", encoding="utf-8") as f:
        f.writelines(json.dumps(c) + "\n" for c in chunks)

    texts = [c["text"] for c in chunks]
    bm = bm25s.BM25()
    bm.index(bm25s.tokenize(texts))
    bm.save(str(d / "bm25"))

    model = SentenceTransformer(MODEL)
    emb = model.encode(["passage: " + t for t in texts], batch_size=64, normalize_embeddings=True,
                       show_progress_bar=True)
    idx = faiss.IndexFlatIP(emb.shape[1])
    idx.add(emb)
    faiss.write_index(idx, str(d / "faiss.index"))
    print(f"{len(chunks)} chunks indexed")
