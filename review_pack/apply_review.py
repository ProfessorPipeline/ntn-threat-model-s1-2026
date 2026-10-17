"""Safely import draft review proposals into the existing S1 project.

Run from the project folder. Preview is the default. --apply makes a backup
then updates only untouched source records. Student results are never created.
"""
import argparse
import hashlib
import json
import shutil
import sqlite3
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PACK = Path(__file__).resolve().parent


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description="Preview or apply the AI-assisted S1 review proposals")
    parser.add_argument("--project", type=Path)
    parser.add_argument("--db", type=Path, help="Database path relative to the project unless absolute")
    parser.add_argument("--apply", action="store_true", help="Back up then apply untouched draft proposals")
    args = parser.parse_args()
    project = (args.project or (Path.cwd() if (Path.cwd()/"run.py").is_file() else PACK.parent)).resolve()
    if not (project/"ntn/repository.py").is_file():
        parser.error("Put review_pack beside run.py or supply --project with the existing project folder")
    db_path = args.db or Path("data/ntn.sqlite3")
    if not db_path.is_absolute():
        db_path = project/db_path
    if not db_path.is_file():
        parser.error("Start the core app once to create its database before importing")
    sys.path.insert(0, str(project))
    from ntn.domain import validate_threat
    from ntn.repository import Repository
    repo = Repository(db_path)
    proposals = read_json(PACK/"data/catalogue-proposals.json")
    original = read_json(PACK/"data/original-seed.json")
    incoming_refs = {s["id"]: s for s in proposals["references"]}
    base_refs = {s["id"]: s for s in original["references"]}
    current_refs = {s["id"]: s for s in repo.references()}
    reference_conflicts = [key for key, current in current_refs.items()
        if key in incoming_refs and current not in [incoming_refs[key], base_refs.get(key)]]
    if reference_conflicts:
        parser.error("Source entries were edited. Merge them manually before applying: " + " / ".join(reference_conflicts))
    ref_ids = set(current_refs) | set(incoming_refs)
    base = {t["id"]: validate_threat(t, ref_ids) for t in original["threats"]}
    current = {t["id"]: t for t in repo.threats()}
    plans = []
    with repo.connection() as db:
        for item in proposals["threats"]:
            proposed = validate_threat(item, ref_ids)
            tid = proposed["id"]
            if proposed["review_status"] != "Draft" or proposed["reviewer"] or proposed["review_date"] or any(e["checked"] for e in proposed["evidence"]):
                parser.error("Proposal data must not claim completed student reviews")
            old = current.get(tid)
            if old is None:
                action = "CREATE"
            elif validate_threat(old, ref_ids) == proposed:
                action = "UNCHANGED"
            elif (old["review_status"] == "Reviewed" or any(e["checked"] for e in old["evidence"])
                  or db.execute("SELECT 1 FROM ratings WHERE threat_id=? LIMIT 1", (tid,)).fetchone()):
                action = "SKIP: student review or ratings exist"
            elif tid in base and validate_threat(old, ref_ids) == base[tid]:
                action = "UPDATE"
            else:
                action = "SKIP: record was edited or ID was reused"
            plans.append((action, proposed, old))
    print("S1 draft review import")
    print("Project:", project)
    print("Database:", db_path)
    for action, proposed, _ in plans:
        print(f"{proposed['id']}: {action} | {proposed['title']}")
    print("No human reviews or student ratings will be generated.")
    if not args.apply:
        print("Preview only. Add --apply after reading the review guide.")
        return
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    backups = project/"backups"/stamp
    backups.mkdir(parents=True, exist_ok=False)
    (backups/"ntn-before-review.sqlite3").write_bytes(repo.snapshot())
    print("Backup:", backups/"ntn-before-review.sqlite3")
    with repo.connection() as db:
        for source in proposals["references"]:
            db.execute("INSERT INTO sources(id,citation,kind,doi,note) VALUES (:id,:citation,:kind,:doi,:note) ON CONFLICT(id) DO UPDATE SET citation=excluded.citation,kind=excluded.kind,doi=excluded.doi,note=excluded.note", source)
        repo._audit(db, "source_preparation", "S1", "AI-assisted source locators imported. Student validation remains pending.")
    for action, proposed, old in plans:
        if action == "CREATE":
            repo.save_threat(proposed, new=True)
        elif action == "UPDATE":
            repo.save_threat({**proposed, "revision": old["revision"]})
    manifest = read_json(PACK/"data/web-patch-manifest.json")
    for relative, hashes in manifest.items():
        target = project/relative
        incoming = PACK/"web_updates"/Path(relative).name
        if target.is_file() and digest(target) == hashes["updated_sha256"]:
            print("Web file already updated:", relative)
        elif target.is_file() and digest(target) == hashes["original_sha256"]:
            backup_file = backups/relative
            backup_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, backup_file)
            shutil.copy2(incoming, target)
            print("Updated web text:", relative)
        else:
            print("Skipped customized web file:", relative, "Merge the wording manually if needed.")
    generator = project/"scripts/build_backup.py"
    if generator.is_file():
        existing = project/"web/backup.html"
        if existing.is_file():
            shutil.copy2(existing, backups/"backup-before-review.html")
        result = subprocess.run([sys.executable, str(generator), "--db", str(db_path)], cwd=project)
        if result.returncode:
            print("The catalogue is imported. Offline snapshot regeneration needs a local check.")
    report = {
        "applied_at": datetime.now(timezone.utc).isoformat(),
        "entries": [{"id": t["id"], "action": action} for action, t, _ in plans],
        "human_reviews_created": 0, "student_ratings_created": 0,
        "record_count_after": len(repo.threats()), "backup": str(backups),
        "notes": "Review the proposed conditions before rating. Skipped custom records need manual comparison. Existing reviewed or rated records are preserved."
    }
    (backups/"import-result.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("Record count:", report["record_count_after"])
    print("Stop and restart the server then refresh the browser. Read docs/START_HERE.md in review_pack.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, sqlite3.Error, ValueError) as error:
        raise SystemExit("Import stopped: " + str(error) + ". Use the saved backup if an applied operation failed.")
