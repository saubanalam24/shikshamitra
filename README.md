# ShikshaMitra

An offline, on-device AI study agent for Snapdragon-powered HP laptops.
Built for the Snapdragon AI Lab Build & Present Challenge.

## The problem

A lot of AI study tools assume you have a fast, always-on internet
connection and don't mind your personal notes going through someone
else's server. Neither of those is a safe assumption for a large chunk
of students in India, especially outside the big metros - patchy mobile
data, and understandable discomfort about uploading your handwritten
notes and doubts to a cloud service.

## The idea

Run the whole thing on the device's own Snapdragon NPU. Chat with an
on-device LLM, search your own notes, auto-generate flashcards, and get
quick calculations done - all with the wifi off. Nothing leaves the
laptop.

## What's actually in here

- **Chat** with a small instruction-tuned model (Phi-3.5-mini or similar)
  served through [GenieX](https://github.com/qualcomm/GenieX), Qualcomm's
  on-device runtime, so inference dispatches to the Hexagon NPU instead of
  burning CPU/battery.
- **Notes search** - drop your own `.txt` notes in `data/sample_notes/`
  and ask things like `search entropy in my notes`. Uses a small local
  TF-IDF index (see `docs/ARCHITECTURE.md` for why not embeddings).
- **Auto flashcards** - `/flashcards <file>` pulls definition-style
  sentences out of your notes and turns them into Q/A pairs.
- **Extractive summarizer** - `/summarize <file>` for a quick recap,
  doesn't even need the LLM loaded.
- **Calculator** - safe expression evaluation for quick doubts.
- Both a Tkinter desktop window and a `--cli` terminal mode.

## Why this fits the challenge

- Optimized for / running on a Snapdragon-powered HP PC (Snapdragon X,
  Hexagon NPU).
- Built around a model sourced from Qualcomm AI Hub, run through GenieX
  on the Hexagon NPU rather than plain CPU inference.
- Genuinely offline and accessible - no subscription, no data plan
  required after setup, works for students with limited or expensive
  connectivity.
- Everything else (search, flashcards, summarizer, calculator) is real,
  runnable, tested code, not just LLM prompt-wrapping - see `tests/`.

## Getting it running

```powershell
git clone <this repo>
cd shikshamitra
.\setup_windows.ps1
```

Then follow `models/README.md` to install GenieX and pick a model - it's
two commands, no manual EP wiring needed.

```powershell
python main.py          # desktop chat window
python main.py --cli     # terminal mode
```

Without a model in `models/llm/`, the app still runs fine - it falls
back to a small stub responder so you can exercise the notes search,
flashcards, summarizer and calculator without needing the ~2-4GB model
files at all (handy for reviewing the code without downloading anything).

## Running the tests

```
pip install -r requirements.txt
pytest tests/ -v
```

9 tests, all covering the parts that don't need the actual model or NPU
hardware to verify: calculator edge cases, the TF-IDF retriever, and the
flashcard generator against the sample notes.

## Project layout

```
main.py                 entry point (GUI by default, --cli for terminal)
config.py                paths and constants
src/
  agent_core.py           routes a message to a tool or to the LLM
  npu_runtime.py           loads the QNN model, falls back to a CPU stub
  tools/
    calculator.py
    note_search.py
    flashcards.py
    summarizer.py
  rag/
    indexer.py             builds the local TF-IDF index
    retriever.py            cosine search over it
  ui/
    desktop_app.py          Tkinter chat window
data/sample_notes/        example lecture notes to try the demo on
models/                    where you drop the AI Hub model export
docs/
  ARCHITECTURE.md
  DEMO_SCRIPT.md
tests/
```

## Honest limitations

- The bundled `data/sample_notes/` are two short example files, real use
  needs the student to drop in their own notes.
- The keyword router for tool calls is intentionally simple rather than
  having the LLM decide - see `docs/ARCHITECTURE.md` for the reasoning.
- The flashcard generator is pattern-based, not a trained model, so it
  works best on notes that actually contain "X is defined as Y" style
  sentences (which lecture notes usually do).
- `npu_runtime.py` is written to the real GenieX Python API
  (`AutoModelForCausalLM.from_pretrained` / `.generate(stream=True)`), and
  was verified against Qualcomm's own GenieX quickstart docs. It falls
  back to a CPU stub gracefully if GenieX or the model isn't set up yet,
  so the rest of the app keeps working either way.

## Author

Sauban Alam, B.S. student, IIT Jodhpur.
