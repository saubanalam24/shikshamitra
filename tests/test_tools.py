import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.tools import calculator, summarizer


def test_calculator_basic():
    assert calculator.calculate("2 + 3 * 4") == 14


def test_calculator_div_by_zero():
    result = calculator.calculate("5 / 0")
    assert "couldn't" in result


def test_calculator_rejects_junk():
    result = calculator.calculate("__import__('os').system('ls')")
    assert "couldn't" in result or "not allowed" in result


def test_summarizer_short_text_passthrough():
    text = "Short sentence. Another one."
    assert summarizer.summarize(text, 5) == text


def test_summarizer_picks_fewer_sentences():
    text = ("Entropy is a measure of disorder. Cats are unrelated to thermodynamics. "
            "The second law says entropy never decreases in an isolated system. "
            "Bananas are yellow.")
    out = summarizer.summarize(text, 2)
    assert "entropy" in out.lower()
    assert len(out.split(". ")) <= 3
