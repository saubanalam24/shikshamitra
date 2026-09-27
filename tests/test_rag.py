import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.rag import indexer, retriever
from src.tools import flashcards


def test_index_builds_from_sample_notes():
    n = indexer.build_index()
    assert n > 0


def test_retriever_finds_relevant_chunk():
    hits = retriever.search("entropy second law")
    assert len(hits) > 0
    assert "entropy" in hits[0][1]["text"].lower()


def test_retriever_empty_query_no_crash():
    hits = retriever.search("")
    assert isinstance(hits, list)


def test_flashcards_generated_from_notes():
    cards = flashcards.make_flashcards("thermodynamics_notes.txt")
    assert len(cards) >= 3
    assert all("q" in c and "a" in c for c in cards)
