import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
NOTES_DIR = os.path.join(BASE_DIR, "data", "sample_notes")
INDEX_DIR = os.path.join(BASE_DIR, "data", "index")

# GenieX model id: either a Qualcomm AI Hub bundle ("ai-hub-models/...",
# runs on the NPU via QAIRT) or a GGUF repo/file ("org/model-gguf", runs
# via llama.cpp, still NPU-capable on Hexagon). Run `geniex model list`
# to see what's available for your chipset before picking one.
GENIEX_MODEL_ID = os.environ.get("SHIKSHAMITRA_MODEL", "ai-hub-models/Phi-3.5-mini-instruct")

# kept for anyone still using the onnxruntime-genai path from models/README.md
LLM_MODEL_DIR = os.path.join(MODELS_DIR, "llm")
EMBED_CACHE_FILE = os.path.join(INDEX_DIR, "notes_index.json")

# how many past turns to keep in context, small on purpose since the
# on-device model runs with a limited context window on NPU
MAX_HISTORY_TURNS = 6

APP_NAME = "ShikshaMitra"
