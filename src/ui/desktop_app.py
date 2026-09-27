import tkinter as tk
from tkinter import scrolledtext
from src import agent_core, npu_runtime
import config


class ChatWindow:
    def __init__(self, root):
        self.root = root
        root.title(config.APP_NAME + " - offline study agent")
        root.geometry("640x520")

        self.log = scrolledtext.ScrolledText(root, state="disabled", wrap="word")
        self.log.pack(fill="both", expand=True, padx=8, pady=8)

        bottom = tk.Frame(root)
        bottom.pack(fill="x", padx=8, pady=(0, 8))

        self.entry = tk.Entry(bottom)
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", lambda e: self.send())

        tk.Button(bottom, text="Send", command=self.send).pack(side="left", padx=(6, 0))

        self._write("system", "Loading model...")
        backend = npu_runtime.init()
        note = "NPU (QNN) model loaded" if backend == "npu" else "no model found in models/llm, running dev stub"
        self._write("system", note)
        self._write("system", "Try: /search entropy   /calc 12*7-4   /flashcards thermodynamics_notes.txt   /summarize thermodynamics_notes.txt")

    def _write(self, who, text):
        self.log.configure(state="normal")
        self.log.insert("end", f"{who}: {text}\n\n")
        self.log.configure(state="disabled")
        self.log.see("end")

    def send(self):
        text = self.entry.get().strip()
        if not text:
            return
        self.entry.delete(0, "end")
        self._write("you", text)
        reply = agent_core.route(text)
        self._write("shikshamitra", reply)


def main():
    root = tk.Tk()
    ChatWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
