"""Run from VS Code or a terminal with Python 3.11 or later."""
import argparse
import sys
from pathlib import Path

if sys.version_info < (3, 11):
    raise SystemExit("Python 3.11 or later is required. Check your version with python --version.")

from ntn.server import make_server

ROOT = Path(__file__).resolve().parent

def main():
    parser = argparse.ArgumentParser(description="Local S1 NTN threat modelling prototype")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--db", type=Path, default=ROOT / "data" / "ntn.sqlite3")
    args = parser.parse_args()
    try:
        server = make_server(args.db, args.host, args.port)
    except OSError as exc:
        parser.exit(1, f"Could not start: {exc}\nTry another port with --port 8001\n")
    print(f"\nS1 NTN threat model: http://127.0.0.1:{server.server_port}\nDatabase: {args.db}\nNo internet or LLM is required. Press Ctrl+C to stop.\n", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.server_close()

if __name__ == "__main__":
    main()
