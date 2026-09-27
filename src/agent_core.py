"""
The actual agent loop. Keeps it simple on purpose - a keyword router picks
a tool when the intent is obvious (search my notes / calculate / flashcards
/ summarize), otherwise the message goes straight to the on-device LLM for
open chat. This avoids relying on the small on-device model to reliably
produce structured function-calling JSON, which quantized 3B models on an
NPU tend to be shaky at anyway.
"""

import os
import re
import config
from src import npu_runtime
from src.tools import calculator, note_search, flashcards, summarizer

_history = []


def _looks_like_math(text):
    return bool(re.search(r"\d.*[\+\-\*/\^].*\d", text)) and any(
        w in text.lower() for w in ["calc", "compute", "what is", "solve", "="]
    )


def route(user_text):
    text = user_text.strip()
    lower = text.lower()

    if lower.startswith("/calc") or _looks_like_math(text):
        expr = text.split("/calc", 1)[-1].strip() if lower.startswith("/calc") else text
        expr = re.sub(r"^(what\s+is|calculate|compute|solve)\s*", "", expr, flags=re.I).rstrip("=? ")
        return f"= {calculator.calculate(expr)}"

    if lower.startswith("/search") or "in my notes" in lower or "from my notes" in lower:
        query = re.sub(r"/search|in my notes|from my notes", "", text, flags=re.I).strip()
        return note_search.search_notes(query)

    if lower.startswith("/flashcards"):
        parts = text.split(" ", 1)
        fname = parts[1].strip() if len(parts) > 1 else "thermodynamics_notes.txt"
        cards = flashcards.make_flashcards(fname)
        if not cards:
            return f"couldn't find definitions to turn into cards in {fname}"
        return "\n".join(f"Q{i+1}: {c['q']}\nA{i+1}: {c['a']}" for i, c in enumerate(cards))

    if lower.startswith("/summarize"):
        fname = text.split(" ", 1)[1].strip() if " " in text else None
        if fname:
            path = os.path.join(config.NOTES_DIR, fname)
            if not os.path.exists(path):
                return f"can't find {fname} in data/sample_notes"
            with open(path, encoding="utf-8") as f:
                content = f.read()
        else:
            content = text
        return summarizer.summarize(content)

    # fall through to the on-device model for general chat / doubts
    return _chat(text)


def _chat(text):
    global _history
    _history.append(("user", text))
    _history = _history[-2 * config.MAX_HISTORY_TURNS:]

    convo = "\n".join(f"{role}: {msg}" for role, msg in _history)
    prompt = (
        "You are ShikshaMitra, an offline study assistant for a college student. "
        "Answer briefly and clearly.\n" + convo + "\nassistant:"
    )
    reply = npu_runtime.generate(prompt)
    _history.append(("assistant", reply))
    return reply
