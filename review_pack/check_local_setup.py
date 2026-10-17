"""Run this on each student's own computer. Performs local software checks only."""
import argparse
import csv
import io
import json
import os
import platform
import queue
import re
import subprocess
import sys
import threading
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--student", required=True, choices=["John", "Marius", "Buildcheck"])
    parser.add_argument("--project", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    project = (args.project or (Path.cwd() if (Path.cwd()/"run.py").is_file() else Path(__file__).resolve().parent.parent)).resolve()
    if not (project/"run.py").is_file():
        parser.error("Run from the project folder or supply --project")
    results = []
    def check(label, condition, detail):
        results.append({"check": label, "passed": bool(condition), "detail": detail})
        print(("PASS " if condition else "FAIL ") + label + " — " + detail)
    check("Python version", sys.version_info >= (3, 11), platform.python_version())
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    proc = subprocess.Popen([sys.executable, str(project/"run.py"), "--port", "0"],
                            cwd=project, env=env, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True, encoding="utf-8")
    lines = queue.Queue()
    def reader():
        for line in proc.stdout:
            lines.put(line)
    thread = threading.Thread(target=reader, daemon=True)
    thread.start()
    try:
        base = None
        deadline = time.monotonic() + 15
        while time.monotonic() < deadline:
            try:
                line = lines.get(timeout=.3)
            except queue.Empty:
                if proc.poll() is not None:
                    break
                continue
            match = re.search(r"http://127\.0\.0\.1:\d+", line)
            if match:
                base = match.group(0)
                break
        if not base:
            raise RuntimeError("The application did not start. Read the normal run.py error in your terminal.")
        def get(path):
            with urllib.request.urlopen(base+path, timeout=8) as response:
                return response.read()
        health = json.loads(get("/api/health"))
        check("Core starts", health.get("status") == "ok", "Entry point launched on a local temporary port")
        check("Core LLM dependency", health.get("llm_required") is False, "Health endpoint reports no LLM requirement")
        model = json.loads(get("/api/model"))
        check("S1 model", len(model["components"]) == 6 and len(model["flows"]) == 5 and len(model["boundaries"]) == 4, "6 components / 5 flow groups / 4 boundaries")
        items = json.loads(get("/api/threats"))["items"]
        check("Review catalogue size", len(items) >= 10, str(len(items)) + " candidates")
        expected = [t["id"] for t in items if "C3" in t["components"] and t["stride"] == "Tampering"]
        filtered = json.loads(get("/api/threats?component=C3&stride=Tampering"))["items"]
        check("Combined filters", [t["id"] for t in filtered] == expected, "C3 + Tampering matches the stored mappings")
        text = get("/api/threats.csv?component=C3&stride=Tampering").decode("utf-8-sig")
        rows = list(csv.DictReader(io.StringIO(text)))
        check("Selected CSV", [r["id"] for r in rows] == expected, "Exported IDs match the API selection")
        values_match = all(str(t["score"] if t["score"] is not None else "") == r["score"] and t["feasibility_reason"] == r["feasibility_reason"] and t["impact_reason"] == r["impact_reason"] for t, r in zip(filtered, rows))
        check("CSV reasons and values", values_match, "Stored scores and reasons are preserved")
        calculated = all(t["score"] == (t["feasibility"]*t["impact"] if t["feasibility"] is not None and t["impact"] is not None else None) for t in items)
        check("Score products", calculated, "F × I matches every scored record")
        coverage = json.loads(get("/api/coverage"))
        check("Worksheet structure", len(coverage["cells"]) == 66 and len(coverage["scope_reviews"]) == 9, "66 cells and 9 asset/boundary review slots")
        check("Offline snapshot file", (project/"web/backup.html").is_file(), "File exists. Browser opening is still a manual check")
        check("Backup endpoint", get("/api/database.sqlite3").startswith(b"SQLite format 3"), "A consistent SQLite backup is available")
    except Exception as error:
        check("Run completed", False, str(error))
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5)
        thread.join(timeout=2)
        proc.stdout.close()
    stamp = datetime.now(timezone.utc)
    report = {"caller_label": args.student, "executed_at": stamp.isoformat(),
              "operating_system": platform.system(), "python_version": platform.python_version(),
              "automated_software_checks_passed": all(x["passed"] for x in results), "checks": results,
              "manual_checks": {"wifi_disconnected": "Pending student test", "offline_viewer_opened_in_browser": "Pending student test", "backup_video_played": "Pending student test"},
              "scope": "Local software checks only. Not an NTN attack experiment or independent scoring result. Caller label is self-declared."}
    target = args.output or (Path(__file__).resolve().parent/"results"/(args.student+"-"+stamp.strftime("%Y%m%dT%H%M%SZ")+".json"))
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("Results:", target)
    print("Now disconnect Wi-Fi and manually open the app and offline viewer. Play the backup video.")
    return 0 if report["automated_software_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
