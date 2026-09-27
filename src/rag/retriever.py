import os
import re
import json
import math
import config
from src.rag.indexer import build_index, _tokenize


def _cosine(a, b):
    common = set(a) & set(b)
    num = sum(a[t] * b[t] for t in common)
    da = math.sqrt(sum(v * v for v in a.values()))
    db = math.sqrt(sum(v * v for v in b.values()))
    if da == 0 or db == 0:
        return 0.0
    return num / (da * db)


def _load_index():
    if not os.path.exists(config.EMBED_CACHE_FILE):
        build_index()
    with open(config.EMBED_CACHE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def search(query, top_k=3):
    idx = _load_index()
    toks = _tokenize(query)
    tf = {}
    for t in toks:
        tf[t] = tf.get(t, 0) + 1
    q_vec = {t: (cnt / len(toks)) * idx["idf"].get(t, 0) for t, cnt in tf.items()} if toks else {}

    scored = []
    for chunk, vec in zip(idx["chunks"], idx["vectors"]):
        s = _cosine(q_vec, vec)
        if s > 0:
            scored.append((s, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_k]


if __name__ == "__main__":
    for score, chunk in search("entropy second law"):
        print(round(score, 3), chunk["source"], "->", chunk["text"][:80])
