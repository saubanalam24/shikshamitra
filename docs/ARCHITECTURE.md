# Architecture

```
                    ┌───────────────────────────┐
                    │   Tkinter desktop window   │
                    │   (or --cli terminal mode) │
                    └────────────┬──────────────┘
                                 │ user text
                                 ▼
                    ┌───────────────────────────┐
                    │        agent_core.py       │
                    │  keyword router:           │
                    │   /calc /search /flashcards│
                    │   /summarize -> tool        │
                    │   anything else -> LLM      │
                    └───┬──────────┬─────────────┘
                        │          │
           ┌────────────┘          └─────────────┐
           ▼                                      ▼
 ┌───────────────────┐                  ┌───────────────────────┐
 │   local tools       │                  │     npu_runtime.py      │
 │  calculator.py       │                  │  GenieX                 │
 │  note_search.py ──┐  │                  │  (Hexagon NPU via QAIRT)│
 │  flashcards.py     │ │                  │  on Snapdragon Hexagon  │
 │  summarizer.py      │ │                  │  NPU (falls back to a   │
 └────────────────────┘ │                  │  CPU stub if no model   │
                         ▼                  │  is present yet)        │
                ┌──────────────────┐        └───────────────────────┘
                │   rag/indexer.py   │
                │   rag/retriever.py │
                │  TF-IDF over the   │
                │  student's own     │
                │  notes, all local  │
                └──────────────────┘
```

## Why this split

The 3B-parameter class of models that currently run well on a Snapdragon
NPU are good conversational models but not reliable at emitting strict
function-calling JSON every time. Rather than betting the whole agent on
that, the obvious intents (do a calculation, search my notes, make
flashcards, summarize this file) are caught by a cheap keyword router
before the message ever reaches the model. Only genuinely open-ended
questions go to the LLM. This keeps the tool calls deterministic and fast,
and reserves the NPU for what it's actually needed for: natural language
answers.

## Why TF-IDF instead of a vector embedding model

Running a second embedding model on top of the LLM eats NPU/RAM budget for
not much benefit at the scale of "one student's semester of notes" (a few
hundred paragraphs at most). A TF-IDF cosine search is fast, has zero
extra memory footprint, needs no download, and is easy to explain to a
judge in one sentence, which mattered more here than chasing a marginal
recall improvement from real embeddings.

## Offline-first, on purpose

Every part of this - the chat, the notes search, the flashcards, the
calculator - runs with no network call at any point. That's the actual
point of the project: a student in an area with patchy or expensive
mobile data still gets a full study companion, and their personal notes
never leave their laptop.
