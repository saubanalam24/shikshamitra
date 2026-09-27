"""
Very small TF-IDF style indexer for the student's own notes.

No embedding model needed (keeps everything CPU-light and fully offline,
no download at first run), just word counts + idf weighting. Good enough
for retrieving the right paragraph out of a semester's worth of notes.
"""

import os
import re
import json
import math
import config


def _tokenize(text):
    return re.findall(r"[a-zA-Z]+", text.lower())


def _load_chunks(notes_dir):
    chunks = []
    for fname in sorted(os.listdir(notes_dir)):
        if not fname.endswith(".txt"):
            continue
        path = os.path.join(notes_dir, fname)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        # split on blank lines -> roughly one chunk per paragraph
        for para in [p.strip() for p in text.split("\n\n") if p.strip()]:
            chunks.append({"source": fname, "text": para})
    return chunks


def build_index(notes_dir=None, out_file=None):
    notes_dir = notes_dir or config.NOTES_DIR
    out_file = out_file or config.EMBED_CACHE_FILE

    chunks = _load_chunks(notes_dir)
    df = {}
    tokenized = []
    for c in chunks:
        toks = _tokenize(c["text"])
        tokenized.append(toks)
        for t in set(toks):
            df[t] = df.get(t, 0) + 1

    n_docs = max(len(chunks), 1)
    idf = {t: math.log(n_docs / (1 + d)) + 1 for t, d in df.items()}

    vectors = []
    for toks in tokenized:
        tf = {}
        for t in toks:
            tf[t] = tf.get(t, 0) + 1
        vec = {t: (cnt / len(toks)) * idf.get(t, 0) for t, cnt in tf.items()} if toks else {}
        vectors.append(vec)

    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({"chunks": chunks, "vectors": vectors, "idf": idf}, f)

    return len(chunks)


if __name__ == "__main__":
    n = build_index()
    print(f"indexed {n} chunks from {config.NOTES_DIR}")
