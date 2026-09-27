# 3-minute demo script

Use this as the talk track for the pitch video / live demo in front of judges.

1. **Hook (15s)** - "This runs a full AI study assistant on a Snapdragon
   laptop with the wifi off. No cloud, no API key, no internet bill."
   Turn off wifi on camera before starting.

2. **Show the app open (10s)** - launch with `python main.py`, point out
   it says "NPU (QNN) model loaded" in the log - this is running on the
   Hexagon NPU, not the CPU.

3. **Notes search (30s)** - type `search entropy in my notes`, show it
   pulling the right paragraph out of the sample thermodynamics notes
   instantly, entirely offline.

4. **Flashcards (25s)** - `/flashcards organic_chem_notes.txt` - show it
   auto-generating Q/A pairs from lecture notes with zero manual tagging.

5. **Open chat (40s)** - ask it an actual doubt, e.g. "explain SN1 vs SN2
   in simple terms" - let the model answer, point out the response is
   coming from the NPU, no network indicator active.

6. **Calculator (15s)** - quick `what is 235*17-40?` to show the tool
   routing working alongside the chat.

7. **Close (15s)** - "Every one of these runs entirely on-device. For a
   student without reliable internet, or one who doesn't want personal
   notes uploaded anywhere, this is a full offline tutor in their pocket."

Total: ~2:30, leaves buffer for the 3-minute cap.
