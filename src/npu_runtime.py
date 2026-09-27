"""
Wraps model loading + text generation for the Snapdragon NPU.

Real path: GenieX (Qualcomm's on-device inference runtime - pip install
geniex), which mirrors the transformers from_pretrained()/.generate() API
and dispatches to the Hexagon NPU automatically. Pointed at a pre-compiled
bundle from Qualcomm AI Hub, it runs on the QAIRT/NPU backend; pointed at
a GGUF file it runs through llama.cpp (still NPU-capable via Hexagon HTP
kernels). Either way it's a couple of lines, no Olive, no manual QNN EP
wiring.

Dev/CPU path: if geniex or the model isn't present (like on this Linux
box while I was writing this, or on someone's non-Snapdragon machine), we
fall back to a tiny local responder so the rest of the app is still
testable without the model downloaded.
"""

import config

_model = None
_backend = None


def init():
    global _model, _backend
    try:
        from geniex import AutoModelForCausalLM

        _model = AutoModelForCausalLM.from_pretrained(config.GENIEX_MODEL_ID)
        _backend = "npu"
        print("[npu_runtime] loaded", config.GENIEX_MODEL_ID, "via GenieX")
        return "npu"
    except Exception as e:
        print("[npu_runtime] falling back to CPU stub -", e)
        _backend = "stub"
        return "cpu-stub"


def generate(prompt, max_tokens=256):
    global _backend
    if _backend is None:
        init()

    if _backend == "stub":
        return _stub_generate(prompt)

    messages = [{"role": "user", "content": prompt}]
    chat_prompt = _model.tokenizer.apply_chat_template(messages, add_generation_prompt=True)

    out = []
    for chunk in _model.generate(chat_prompt, max_new_tokens=max_tokens, stream=True):
        out.append(chunk)
    return "".join(out)


def _stub_generate(prompt):
    # not the real model -- just enough to keep the agent loop and UI
    # working while GenieX / the model isn't set up yet. swap this out
    # once `pip install geniex` + a downloaded model are in place
    lower = prompt.lower()
    if "hi" in lower or "hello" in lower:
        return "Hey, I'm running in offline stub mode right now (GenieX/model not set up). Ask me something and I'll at least try."
    return ("(stub reply - install geniex and set config.GENIEX_MODEL_ID for real answers) "
            "I heard: " + prompt[-200:])
