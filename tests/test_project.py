"""Meaningful end-to-end checks using only Python's standard library.

All data written by these tests lives in a temporary database.
No fabricated ratings enter the delivered research database.
"""
import copy
import csv
import io
import json
import sqlite3
import tempfile
import threading
import unittest
from datetime import date
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from ntn.domain import Conflict, Invalid
from ntn.repository import Repository
from ntn.server import csv_bytes, make_server


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "test.sqlite3"
        self.repo = Repository(self.path)

    def tearDown(self):
        self.temp.cleanup()

    def rating(self, tid="T-02", rater="John", f=2, i=4, revision=1):
        return {"threat_id": tid, "revision": revision, "rater": rater,
                "feasibility": f, "impact": i,
                "feasibility_reason": "TEST ONLY: privileged access is required.",
                "impact_reason": "TEST ONLY: ground administration is affected."}

    def test_seed_provenance_and_no_invented_results(self):
        threats = self.repo.threats()
        self.assertEqual(len(threats), 7)
        self.assertEqual([(t["id"], t["score"], t["band"]) for t in threats],
                         [("T-02", 8, "High"), ("T-01", 6, "Medium"),
                          ("T-04", 6, "Medium"), ("T-05", 6, "Medium"),
                          ("T-03", 6, "Medium"), ("T-06", None, "Unscored"),
                          ("T-07", None, "Unscored")])
        self.assertTrue(all(t["review_status"] != "Reviewed" for t in threats))
        self.assertFalse(any(e["checked"] for t in threats for e in t["evidence"]))
        self.assertEqual(self.repo.coverage()["completed"], 0)
        self.assertEqual(self.repo.consistency("John")["pairs"], 0)
        self.assertIsNone(self.repo.consistency("John")["impact_percent"])

    def test_filter_intersection_and_csv_values(self):
        query = {"component": "C3", "stride": "Tampering"}
        records = self.repo.threats(query)
        self.assertEqual([t["id"] for t in records], ["T-02"])
        rows = list(csv.DictReader(io.StringIO(csv_bytes(records).decode("utf-8-sig"))))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["score"], "8")
        self.assertEqual(json.loads(rows[0]["flows"]), ["F3", "F5"])
        self.assertIn("Privileged access", rows[0]["feasibility_reason"])
        self.assertEqual(rows[0]["description"], records[0]["description"])
        self.assertEqual(self.repo.threats({"component": "C1", "stride": "Repudiation"}), [])
        with self.assertRaises(Invalid):
            self.repo.threats({"component": "C99"})

    def test_all_matrix_bands_via_persisted_records(self):
        # Test externally specified expectations for every matrix coordinate.
        expected = [["Low", "Low", "Low", "Medium"],
                    ["Low", "Medium", "Medium", "High"],
                    ["Low", "Medium", "High", "Critical"],
                    ["Medium", "High", "Critical", "Critical"]]
        for f in range(1, 5):
            for i in range(1, 5):
                t = self.repo.threat("T-02")
                t.update(feasibility=f, impact=i)
                saved = self.repo.save_threat(t)
                self.assertEqual(saved["score"], f * i)
                self.assertEqual(saved["band"], expected[f-1][i-1])

    def test_validate_ratings_mappings_sources_and_review(self):
        t = self.repo.threat("T-02")
        bad_cases = [{"feasibility": True}, {"impact": 5}, {"components": ["C99"]},
                     {"feasibility": None}, {"confidence": "Certain"},
                     {"review_status": "Reviewed", "reviewer": "", "review_date": ""}]
        for changes in bad_cases:
            with self.subTest(changes=changes), self.assertRaises(Invalid):
                self.repo.save_threat({**t, **changes})
        invalid = copy.deepcopy(t)
        invalid["evidence"][0].update(checked=True, reference_id="R1", locator="", checked_by="John", checked_date=date.today().isoformat())
        with self.assertRaises(Invalid):
            self.repo.save_threat(invalid)
        invalid["evidence"][0].update(checked=False, reference_id="R99")
        with self.assertRaises(Invalid):
            self.repo.save_threat(invalid)

    def test_persistence_and_edit_conflict(self):
        t = self.repo.threat("T-02")
        t["title"] = "TEST ONLY: changed title"
        changed = self.repo.save_threat(t)
        self.assertEqual(changed["revision"], 2)
        self.assertEqual(Repository(self.path).threat("T-02")["title"], t["title"])
        with self.assertRaises(Conflict):
            self.repo.save_threat(t)
        with self.assertRaises(Conflict):
            self.repo.save_threat(t, new=True)

    def test_blind_locked_initial_ratings_and_revision_history(self):
        self.repo.submit_rating(self.rating())
        marius = self.repo.consistency("Marius")
        row = next(r for r in marius["records"] if r["id"] == "T-02")
        self.assertEqual(row["ratings"], [])
        with self.assertRaises(Conflict):
            self.repo.submit_rating(self.rating(f=3))
        self.repo.submit_rating(self.rating(rater="Marius", f=3))
        result = self.repo.consistency("John")
        self.assertEqual(result["pairs"], 1)
        self.assertEqual(result["feasibility_percent"], 0)
        self.assertEqual(result["impact_percent"], 100)
        self.repo.save_consensus({"threat_id": "T-02", "revision": 1, "outcome": "Agreed",
                                  "feasibility": 2, "impact": 4, "reason": "TEST ONLY: applied privileged access criterion.",
                                  "criterion": "F2 privileged access", "recorded_by": "TEST ONLY: both students"})
        t = self.repo.threat("T-02")
        self.repo.save_threat({**t, "title": t["title"] + " TEST"})
        self.assertEqual(self.repo.consistency("John")["pairs"], 0)
        exported = self.repo.evaluation_export()
        self.assertEqual(len(exported["initial_ratings"]), 2)
        self.assertEqual(len(exported["consensus"]), 1)

    def test_agreement_denominator_and_escalation(self):
        for tid in ["T-01", "T-02"]:
            self.repo.submit_rating(self.rating(tid, "John", 2, 3))
            self.repo.submit_rating(self.rating(tid, "Marius", 2, 3 if tid == "T-01" else 4))
        self.repo.submit_rating(self.rating("T-03", "John", 3, 2))
        result = self.repo.consistency("Marius")
        self.assertEqual(result["pairs"], 2)
        self.assertEqual(result["feasibility_percent"], 100)
        self.assertEqual(result["impact_percent"], 50)
        self.repo.save_consensus({"threat_id": "T-02", "revision": 1, "outcome": "Escalated",
                                  "reason": "TEST ONLY: disagreement needs supervisor feedback.",
                                  "criterion": "I3 scope versus I4 ground administration", "recorded_by": "TEST ONLY"})
        self.assertEqual(self.repo.consistency("John")["escalated"], 1)
        self.assertEqual(self.repo.threat("T-02")["score"], 8)

    def test_coverage_requires_matching_mapping_and_human_outcome(self):
        cells = self.repo.coverage()["cells"]
        self.assertEqual(len(cells), 66)
        c = next(c for c in cells if c["entity"] == "C3" and c["stride"] == "Tampering")
        self.assertEqual(c["status"], "Pending")
        self.assertEqual(c["candidates"], ["T-02"])
        data = {**c, "status": "Linked", "threat_ids": ["T-02"], "reason": "TEST ONLY: reviewed matching candidate.", "reviewer": "TEST ONLY", "review_date": date.today().isoformat()}
        self.repo.save_coverage(data)
        self.assertEqual(self.repo.coverage()["completed"], 1)
        with self.assertRaises(Conflict):
            self.repo.save_coverage(data)
        other = next(c for c in cells if c["entity"] == "C1" and c["stride"] == "Tampering")
        with self.assertRaises(Invalid):
            self.repo.save_coverage({**data, **other, "status": "Linked", "threat_ids": ["T-02"]})
        self.repo.save_threat(self.repo.threat("T-02"))
        self.assertEqual(self.repo.coverage()["completed"], 0)

    def test_new_candidate_invalidates_prior_no_threat_outcome(self):
        cell = next(c for c in self.repo.coverage()["cells"] if c["entity"] == "C3" and c["stride"] == "Tampering")
        self.repo.save_coverage({**cell, "status": "No applicable threat", "reason": "TEST ONLY: provisional review.", "reviewer": "TEST ONLY", "review_date": date.today().isoformat()})
        new = self.repo.threat("T-02")
        new.update(id="T-08", title="TEST ONLY: additional matching candidate")
        self.repo.save_threat(new, new=True)
        self.assertEqual(self.repo.coverage()["completed"], 0)

    def test_backup_is_valid_sqlite_and_formula_csv_is_safe(self):
        blob = self.repo.snapshot()
        backup = Path(self.temp.name) / "backup.sqlite3"
        backup.write_bytes(blob)
        with sqlite3.connect(backup) as db:
            self.assertEqual(db.execute("PRAGMA integrity_check").fetchone()[0], "ok")
            self.assertEqual(db.execute("SELECT COUNT(*) FROM threats").fetchone()[0], 7)
        t = self.repo.threat("T-02")
        t["title"] = '=HYPERLINK("https://example.invalid")'
        csv_text = csv_bytes([t]).decode("utf-8-sig")
        row = next(csv.DictReader(io.StringIO(csv_text)))
        self.assertTrue(row["title"].startswith("'="))


class HTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.server = make_server(Path(cls.temp.name) / "http.sqlite3", port=0)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = "http://127.0.0.1:" + str(cls.server.server_port)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()
        cls.temp.cleanup()

    def request(self, path, body=None, headers=None):
        req = Request(self.base + path, data=json.dumps(body).encode() if body is not None else None,
                      headers=headers or {})
        try:
            with urlopen(req, timeout=5) as response:
                return response.status, response.headers, response.read()
        except HTTPError as error:
            return error.code, error.headers, error.read()

    def test_browser_assets_api_and_filtered_export(self):
        for path in ["/", "/app.js", "/style.css", "/architecture.svg", "/backup.html", "/api/model", "/api/health", "/api/references", "/api/openapi.json"]:
            with self.subTest(path=path):
                self.assertEqual(self.request(path)[0], 200)
        result = json.loads(self.request("/api/threats?component=C3&stride=Tampering")[2])
        self.assertEqual([x["id"] for x in result["items"]], ["T-02"])
        text = self.request("/api/threats.csv?component=C3&stride=Tampering")[2].decode("utf-8-sig")
        self.assertEqual([x["id"] for x in csv.DictReader(io.StringIO(text))], ["T-02"])

    def test_invalid_requests_and_local_write_boundary(self):
        self.assertEqual(self.request("/api/threats?component=C99")[0], 400)
        self.assertEqual(self.request("/api/threats?component=C1&component=C2")[0], 400)
        self.assertEqual(self.request("/api/consistency")[0], 400)
        self.assertEqual(self.request("/api/threats/T-99")[0], 404)
        self.assertEqual(self.request("/../run.py")[0], 404)
        self.assertEqual(self.request("/api/threats", headers={"Host": "untrusted.invalid"})[0], 400)
        self.assertEqual(self.request("/api/ratings", body={})[0], 400)
        self.assertEqual(self.request("/api/ratings", body={}, headers={"Content-Type": "application/json", "X-NTN-Local": "1", "Origin": "https://untrusted.invalid"})[0], 400)

    def test_write_read_persistence_and_backup_routes(self):
        rating = {"threat_id": "T-01", "revision": 1, "rater": "John", "feasibility": 2, "impact": 3,
                  "feasibility_reason": "TEST ONLY: specialist equipment.", "impact_reason": "TEST ONLY: shared service."}
        headers = {"Content-Type": "application/json", "X-NTN-Local": "1"}
        self.assertEqual(self.request("/api/ratings", rating, headers)[0], 201)
        self.assertEqual(self.request("/api/ratings", rating, headers)[0], 409)
        data = json.loads(self.request("/api/consistency?rater=Marius")[2])
        self.assertEqual(next(r for r in data["records"] if r["id"] == "T-01")["ratings"], [])
        self.assertTrue(self.request("/api/database.sqlite3")[2].startswith(b"SQLite format 3"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
