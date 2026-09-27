"""
Plain extractive summarizer, word-frequency based (Luhn-ish). Runs on pure
python, no model needed, so it works even before/without the NPU model is
loaded - handy for quick note review while the LLM is still loading.
"""

import re

STOPWORDS = set("""
the a an is are was were be been being of to in on for and or but with as
at by from this that these those it its it's into over under after before
than then so not no do does did can could should would may might will
""".split())


def _sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]


def summarize(text, n_sentences=3):
    sents = _sentences(text)
    if len(sents) <= n_sentences:
        return text.strip()

    freq = {}
    for sent in sents:
        for w in re.findall(r"[a-zA-Z]+", sent.lower()):
            if w in STOPWORDS:
                continue
            freq[w] = freq.get(w, 0) + 1

    if not freq:
        return " ".join(sents[:n_sentences])

    max_f = max(freq.values())
    for w in freq:
        freq[w] /= max_f

    scored = []
    for i, sent in enumerate(sents):
        words = re.findall(r"[a-zA-Z]+", sent.lower())
        score = sum(freq.get(w, 0) for w in words)
        scored.append((score, i, sent))

    top = sorted(scored, key=lambda x: x[0], reverse=True)[:n_sentences]
    top.sort(key=lambda x: x[1])  # put back in original order
    return " ".join(s for _, _, s in top)


if __name__ == "__main__":
    sample = ("The second law of thermodynamics states that the total entropy of an "
              "isolated system can never decrease over time. Entropy is often described "
              "as a measure of disorder. In practical terms this means no engine can be "
              "100 percent efficient, some energy is always lost as heat.")
    print(summarize(sample, 2))
