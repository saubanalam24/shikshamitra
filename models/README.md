# getting a real model running on the NPU

## The easy way: GenieX (recommended)

Qualcomm ships a runtime called GenieX specifically so you don't have to
deal with Olive/QAIRT/manual EP wiring. It's two commands.

### 1. Install

```powershell
# download & run the installer from https://github.com/qualcomm/GenieX/releases
# (Windows ARM64 installer), then open a NEW terminal so PATH picks it up
pip install geniex
```

### 2. Quick sanity check it's actually using the NPU

```powershell
geniex infer google/gemma-4-E4B-it-qat-q4_0-gguf
```

If that gives you a real chat response, GenieX + your Snapdragon NPU are
working end to end.

### 3. Get a model for ShikshaMitra

```powershell
geniex model list
```

This browses every Qualcomm AI Hub bundle available for your specific
chipset (highest NPU performance). Pick one close to `Phi-3.5-mini-instruct`
or `Llama-3.2-3B` if available, or use any GGUF from Hugging Face for
broader model choice (still NPU-capable via Hexagon HTP kernels in
llama.cpp) - just pick `Q4_0` precision if asked, it has the best NPU
support.

Set the exact id in `config.py` (`GENIEX_MODEL_ID`) or via an environment
variable so you don't have to edit code:

```powershell
$env:SHIKSHAMITRA_MODEL = "ai-hub-models/Phi-3.5-mini-instruct"
python main.py
```

`npu_runtime.py` calls `AutoModelForCausalLM.from_pretrained(...)` on that
id and GenieX handles the rest (download, compile if needed, dispatch to
the Hexagon NPU). If it's missing or fails to load for any reason, the app
falls back to a CPU stub so notes search / flashcards / summarizer /
calculator keep working while you sort the model out.

## The hard way: onnxruntime-genai + manual QNN EP

This is what the code originally targeted before we found GenieX. It
still works, but it's a lot more moving parts (a separate `onnxruntime-qnn`
package, and - critically - the standard `onnxruntime_genai.models.builder`
tool does NOT support `-e qnn` as a target; getting a QNN-targeted ONNX
export requires Microsoft's Olive with Qualcomm's QAIRT recipe pipeline,
which is a heavier, separate toolchain). Only worth it if you specifically
need the onnxruntime-genai API surface for some reason. Not recommended
under a tight deadline - use GenieX above instead.
