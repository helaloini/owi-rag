import json
from pathlib import Path

from .index import MODEL

DEPTH = 50  # candidates taken from each ranker before fusion


def rrf(rankings, k=60):
    """Reciprocal Rank Fusion over lists of ids; returns ids best-first."""
    score = {}
    for ranking in rankings:
        for rank, i in enumerate(ranking):
            score[i] = score.get(i, 0) + 1 / (k + rank + 1)
    return sorted(score, key=score.get, reverse=True)


class Retriever:
    def __init__(self, data="data"):
        import bm25s
        import faiss
        from sentence_transformers import SentenceTransformer

        d = Path(data)
        with open(d / "chunks.jsonl", encoding="utf-8") as f:
            self.chunks = [json.loads(line) for line in f]
        self._bm25 = bm25s.BM25.load(str(d / "bm25"))
        self._faiss = faiss.read_index(str(d / "faiss.index"))
        self._model = SentenceTransformer(MODEL)
        self._tokenize = bm25s.tokenize

    def _sparse(self, q, k):
        docs = self._bm25.retrieve(self._tokenize(q, return_ids=False), k=min(k, len(self.chunks)))
        return [int(i) for i in docs.documents[0]]

    def _dense(self, q, k):
        emb = self._model.encode(["query: " + q], normalize_embeddings=True)
        _, ids = self._faiss.search(emb, k)
        return [int(i) for i in ids[0] if i >= 0]

    def search(self, mode, q, k=10):
        """mode: bm25 | dense | hybrid. Returns chunk dicts, best first."""
        if mode == "bm25":
            ids = self._sparse(q, k)
        elif mode == "dense":
            ids = self._dense(q, k)
        else:
            ids = rrf([self._sparse(q, DEPTH), self._dense(q, DEPTH)])[:k]
        return [self.chunks[i] for i in ids]
