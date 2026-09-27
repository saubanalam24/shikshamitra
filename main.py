import argparse
from src import agent_core, npu_runtime


def cli_loop():
    backend = npu_runtime.init()
    print(f"[main] backend: {backend}")
    print("ShikshaMitra CLI. Ctrl+C to quit.")
    print("commands: /search <q>  /calc <expr>  /flashcards <file>  /summarize <file>")
    while True:
        try:
            text = input("you> ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            break
        if not text:
            continue
        print("bot>", agent_core.route(text))


def main():
    parser = argparse.ArgumentParser(description=f"{'ShikshaMitra'} offline study agent")
    parser.add_argument("--cli", action="store_true", help="run in terminal instead of the desktop window")
    args = parser.parse_args()

    if args.cli:
        cli_loop()
    else:
        from src.ui.desktop_app import main as gui_main
        gui_main()


if __name__ == "__main__":
    main()
