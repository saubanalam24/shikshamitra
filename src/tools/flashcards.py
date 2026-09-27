"""
Quick and dirty flashcard generator. Looks for definition-style sentences
("X is Y", "X refers to Y", "X means Y") in a notes file and turns them
into Q/A pairs. Not fancy NLP, just regex + a bit of cleanup, but it does
the job for lecture-note style text without needing the LLM at all.
"""

import os
import re
import config

PATTERNS = [
    re.compile(r"^([A-Z][A-Za-z0-9\-\s]{2,40}?)\s+(?:is|are)\s+(?:defined as|described as)\s+(.+)$"),
    re.compile(r"^([A-Z][A-Za-z0-9\-\s]{2,40}?)\s+refers to\s+(.+)$"),
    re.compile(r"^([A-Z][A-Za-z0-9\-\s]{2,40}?)\s+means\s+(.+)$"),
    re.compile(r"^([A-Z][A-Za-z0-9\-\s]{2,40}?)\s+is\s+(?:a|an|the)\s+(.+)$"),
]


BAD_STARTS = {"in", "this", "it", "there", "that", "these", "those", "when", "while", "if", "so"}


def _sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]


def _looks_like_a_term(term):
    words = term.split()
    if len(words) > 6:
        return False
    if words[0].lower() in BAD_STARTS:
        return False
    return True


def make_flashcards(filename, max_cards=10):
    path = os.path.join(config.NOTES_DIR, filename)
    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    cards = []
    for sent in _sentences(text):
        for pat in PATTERNS:
            m = pat.match(sent)
            if m:
                term, definition = m.group(1).strip(), m.group(2).strip().rstrip(".")
                if not _looks_like_a_term(term):
                    continue
                cards.append({"q": f"What {'is' if len(term.split()) < 4 else 'are'} {term}?", "a": definition})
                break
        if len(cards) >= max_cards:
            break

    return cards


if __name__ == "__main__":
    for c in make_flashcards("thermodynamics_notes.txt"):
        print("Q:", c["q"])
        print("A:", c["a"])
        print()
