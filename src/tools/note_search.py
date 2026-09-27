from src.rag import retriever


def search_notes(query, top_k=3):
    hits = retriever.search(query, top_k=top_k)
    if not hits:
        return "nothing in your notes matches that, try rephrasing"

    lines = []
    for score, chunk in hits:
        snippet = chunk["text"].strip().replace("\n", " ")
        if len(snippet) > 220:
            snippet = snippet[:220] + "..."
        lines.append(f"[{chunk['source']}] {snippet}")
    return "\n".join(lines)
