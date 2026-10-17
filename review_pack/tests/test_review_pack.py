"""Tests use disposable databases. They do not create real student results."""
import copy
import hashlib
import json
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

PACK = Path(__file__).resolve().parents[1]
PARENT = PACK.parent
PROJECT = PARENT if (PARENT/"ntn/repository.py").is_file() else PARENT/"ntn-threat-model"
sys.path.insert(0, str(PROJECT))
from ntn.domain import STRIDE, validate_threat
from ntn.repository import Repository


class ProposalTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((PACK/"data/catalogue-proposals.json").read_text(encoding="utf-8"))

    def test_ten_valid_drafts_with_no_completed_student_checks(self):
        refs = {r["id"] for r in self.data["references"]}
        threats = [validate_threat(t, refs) for t in self.data["threats"]]
        self.assertEqual(len(threats), 10)
        self.assertEqual({t["stride"] for t in threats}, set(STRIDE))
        for t in threats:
            self.assertEqual(t["review_status"], "Draft")
            self.assertEqual(t["reviewer"], "")
            self.assertEqual(t["review_date"], "")
            self.assertEqual(t["confidence"], "Low")
            self.assertIsNotNone(t["feasibility"])
            self.assertTrue(all(not e["checked"] and not e["checked_by"] for e in t["evidence"]))

    def test_tpm_replacement_and_rating_changes_are_explicit(self):
        t = {x["id"]: x for x in self.data["threats"]}
        self.assertFalse(any("TPM" in m["text"] for m in t["T-02"]["mitigations"]))
        self.assertTrue(any("CM-3" in m["note"] for m in t["T-02"]["mitigations"]))
        self.assertEqual((t["T-03"]["feasibility"], t["T-03"]["impact"]), (2, 2))
        self.assertEqual((t["T-05"]["feasibility"], t["T-05"]["impact"]), (2, 2))
        self.assertEqual((t["T-06"]["feasibility"], t["T-06"]["impact"]), (2, 3))
        self.assertEqual((t["T-07"]["feasibility"], t["T-07"]["impact"]), (2, 4))

    def test_nist_locators_match_the_checked_control_set(self):
        metadata = json.loads((PACK/"data/source-check-metadata.json").read_text())
        allowed = set(metadata["checked_control_ids"])
        for t in self.data["threats"]:
            for e in t["evidence"]:
                if e["reference_id"] == "R8":
                    found = set(re.findall(r"\b[A-Z]{2}-\d+(?:\(\d+\))?", e["locator"]))
                    self.assertTrue(found)
                    self.assertFalse(found - allowed)

    def test_all_66_proposal_positions_and_nine_scope_prompts(self):
        cells = json.loads((PACK/"data/coverage-proposals.json").read_text(encoding="utf-8"))
        self.assertEqual(len(cells), 66)
        self.assertEqual(len({(c["entity"], c["stride"]) for c in cells}), 66)
        threats = {t["id"]: t for t in self.data["threats"]}
        for c in cells:
            self.assertEqual(c["student_review_status"], "Pending")
            self.assertFalse(c["reviewer"] or c["review_date"])
            self.assertTrue(c["reason"])
            for tid in c["threat_ids"]:
                t = threats[tid]
                self.assertEqual(t["stride"], c["stride"])
                self.assertIn(c["entity"], t["components"] + t["flows"])
        self.assertEqual(sum(c["suggested_outcome"] == "Research question — pending" for c in cells), 14)
        scope = json.loads((PACK/"data/scope-review-proposals.json").read_text(encoding="utf-8"))
        self.assertEqual(len(scope), 9)
        self.assertTrue(all(s["status"] == "Pending" and not s["reviewer"] for s in scope))


class ImportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.project = Path(self.temp.name)/"ntn-threat-model"
        shutil.copytree(PROJECT, self.project, ignore=shutil.ignore_patterns("review_pack", "docs", "evidence", "backups", "__pycache__", "*.pyc", "*.sqlite3*"))
        self.db_path = self.project/"data/ntn.sqlite3"
        self.repo = Repository(self.db_path)

    def tearDown(self):
        self.temp.cleanup()

    def run_import(self, apply=True):
        args = [sys.executable, str(PACK/"apply_review.py"), "--project", str(self.project)]
        if apply:
            args.append("--apply")
        return subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8", timeout=20)

    def test_preview_preserves_records_and_results(self):
        initial = self.repo.threats()
        result = self.run_import(False)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(initial, self.repo.threats())
        self.assertFalse((self.project/"backups").exists())
        self.assertEqual(self.repo.consistency("John")["pairs"], 0)

    def test_import_creates_ten_drafts_and_a_seven_record_backup(self):
        result = self.run_import()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(len(self.repo.threats()), 10)
        self.assertEqual(len(self.repo.references()), 12)
        self.assertEqual(self.repo.coverage()["completed"], 0)
        self.assertEqual(self.repo.consistency("John")["pairs"], 0)
        self.assertFalse(self.repo.evaluation_export()["initial_ratings"])
        self.assertTrue(all(t["review_status"] == "Draft" for t in self.repo.threats()))
        backup = next((self.project/"backups").glob("*/ntn-before-review.sqlite3"))
        with sqlite3.connect(backup) as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM threats").fetchone()[0], 7)
            self.assertEqual(db.execute("PRAGMA integrity_check").fetchone()[0], "ok")
        html = (self.project/"web/backup.html").read_text(encoding="utf-8")
        self.assertIn('"id": "T-10"', html)

    def test_second_import_does_not_bump_record_revisions(self):
        self.assertEqual(self.run_import().returncode, 0)
        revisions = {t["id"]: t["revision"] for t in self.repo.threats()}
        again = self.run_import()
        self.assertEqual(again.returncode, 0, again.stdout)
        self.assertEqual(revisions, {t["id"]: t["revision"] for t in self.repo.threats()})

    def test_custom_record_is_not_overwritten(self):
        t = self.repo.threat("T-02")
        self.repo.save_threat({**t, "title": "TEST ONLY: student edited title"})
        result = self.run_import()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("T-02: SKIP", result.stdout)
        self.assertEqual(self.repo.threat("T-02")["title"], "TEST ONLY: student edited title")

    def test_rated_record_is_not_overwritten(self):
        self.repo.submit_rating({"threat_id": "T-02", "revision": 1, "rater": "John", "feasibility": 2, "impact": 4,
            "feasibility_reason": "TEST ONLY: temporary database.", "impact_reason": "TEST ONLY: temporary database."})
        result = self.run_import()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("T-02: SKIP", result.stdout)
        self.assertEqual(self.repo.threat("T-02")["revision"], 1)
        self.assertEqual(len(self.repo.evaluation_export()["initial_ratings"]), 1)

    def test_human_reviewed_record_is_not_overwritten(self):
        t = self.repo.threat("T-02")
        self.repo.save_threat({**t, "review_status": "Reviewed", "reviewer": "TEST ONLY: disposable data", "review_date": date.today().isoformat()})
        result = self.run_import()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(self.repo.threat("T-02")["review_status"], "Reviewed")

    def test_reused_new_id_is_preserved(self):
        t = self.repo.threat("T-01")
        self.repo.save_threat({**t, "id": "T-08", "title": "TEST ONLY: existing different record"}, new=True)
        result = self.run_import()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(self.repo.threat("T-08")["title"], "TEST ONLY: existing different record")

    def test_custom_source_causes_safe_stop(self):
        with self.repo.connection() as db:
            db.execute("UPDATE sources SET note='TEST ONLY: existing source edit' WHERE id='R1'")
        result = self.run_import()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(len(self.repo.threats()), 7)
        self.assertFalse((self.project/"backups").exists())

    def test_customized_web_file_is_preserved(self):
        web = self.project/"web/app.js"
        content = web.read_bytes() + b"\n// TEST ONLY: existing student edit\n"
        web.write_bytes(content)
        result = self.run_import()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(web.read_bytes(), content)
        self.assertEqual(len(self.repo.threats()), 10)


if __name__ == "__main__":
    unittest.main(verbosity=2)
