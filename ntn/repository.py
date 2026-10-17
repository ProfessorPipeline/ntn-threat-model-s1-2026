"""SQLite persistence. Stored judgments stay separate from calculated priority."""
import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

from .domain import (ASSETS, BOUNDARIES, COMPONENTS, FLOWS, MODEL, STRIDE,
                     Conflict, Invalid, priority, rating, required_text,
                     valid_date, validate_threat)


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class Repository:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as db:
            db.executescript(Path(__file__).with_name("schema.sql").read_text(encoding="utf-8"))
            db.execute("PRAGMA journal_mode=WAL")
            if not db.execute("SELECT 1 FROM meta WHERE key='schema_version'").fetchone():
                for kind, items in [("components", COMPONENTS), ("flows", FLOWS),
                                    ("assets", ASSETS), ("boundaries", BOUNDARIES)]:
                    db.executemany("INSERT INTO architecture VALUES (?,?,?)",
                                   [(kind, x["id"], x["name"]) for x in items])
                seed = json.loads(Path(__file__).parent.parent.joinpath("data/seed.json").read_text(encoding="utf-8"))
                for src in seed["references"]:
                    db.execute("INSERT INTO sources VALUES (:id,:citation,:kind,:doi,:note)", src)
                refs = {s["id"] for s in seed["references"]}
                for item in seed["threats"]:
                    self._write_threat(db, validate_threat(item, refs), 1)
                db.executemany("INSERT INTO coverage(entity,stride) VALUES (?,?)",
                               [(x["id"], s) for x in COMPONENTS + FLOWS for s in STRIDE])
                db.executemany("INSERT INTO scope_reviews(entity) VALUES (?)",
                               [(x["id"],) for x in ASSETS + BOUNDARIES])
                db.execute("INSERT INTO meta VALUES ('schema_version','1')")
                self._audit(db, "initialise", "S1", "Imported supplied records. No human reviews or ratings created.")

    @contextmanager
    def connection(self):
        db = sqlite3.connect(self.path, timeout=10)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys=ON")
        try:
            with db:
                yield db
        finally:
            db.close()

    @staticmethod
    def _audit(db, action, target, detail):
        db.execute("INSERT INTO audit(action,target,at,detail) VALUES (?,?,?,?)",
                   (action, target, now(), detail))

    @staticmethod
    def _write_threat(db, threat, revision):
        item = {k: v for k, v in threat.items() if k not in ["components", "assets", "flows", "boundaries", "evidence", "mitigations"]}
        item.update(revision=revision, updated_at=now())
        if revision == 1:
            names = ",".join(item)
            db.execute(f"INSERT INTO threats({names}) VALUES ({','.join('?' for _ in item)})", list(item.values()))
        else:
            db.execute(f"UPDATE threats SET {','.join(k+'=?' for k in item if k != 'id')} WHERE id=?",
                       [v for k, v in item.items() if k != "id"] + [item["id"]])
            for table in ["mappings", "evidence", "mitigations"]:
                db.execute(f"DELETE FROM {table} WHERE threat_id=?", (item["id"],))
        for kind in ["components", "assets", "flows", "boundaries"]:
            db.executemany("INSERT INTO mappings VALUES (?,?,?)", [(item["id"], kind, x) for x in threat[kind]])
        for e in threat["evidence"]:
            db.execute("INSERT INTO evidence(threat_id,reference_id,basis,locator,checked,checked_by,checked_date,note) VALUES (?,?,?,?,?,?,?,?)",
                       (item["id"], e["reference_id"], e["basis"], e["locator"], e["checked"], e["checked_by"], e["checked_date"], e["note"]))
        for m in threat["mitigations"]:
            db.execute("INSERT INTO mitigations(threat_id,text,reference_id,note) VALUES (?,?,?,?)",
                       (item["id"], m["text"], m["reference_id"], m["note"]))

    def references(self):
        with self.connection() as db:
            return [dict(r) for r in db.execute("SELECT * FROM sources ORDER BY id")]

    def threats(self, filters=None):
        filters = filters or {}
        allowed = {"component", "stride", "band", "confidence", "review_status", "q"}
        if set(filters) - allowed:
            raise Invalid("Unknown filter")
        if filters.get("component") and filters["component"] not in {x["id"] for x in COMPONENTS}:
            raise Invalid("Unknown component")
        if filters.get("stride") and filters["stride"] not in STRIDE:
            raise Invalid("Unknown STRIDE category")
        for key, values in {"band": ["Low", "Medium", "High", "Critical", "Unscored"],
                            "confidence": ["Low", "Medium", "High"],
                            "review_status": ["Imported", "Draft", "Reviewed"]}.items():
            if filters.get(key) and filters[key] not in values:
                raise Invalid(f"Unknown {key}")
        with self.connection() as db:
            result = []
            for row in db.execute("SELECT * FROM threats"):
                t = dict(row)
                for kind in ["components", "assets", "flows", "boundaries"]:
                    t[kind] = [r[0] for r in db.execute("SELECT ref_id FROM mappings WHERE threat_id=? AND kind=? ORDER BY ref_id", (t["id"], kind))]
                t["evidence"] = [dict(r) for r in db.execute("SELECT reference_id,basis,locator,checked,checked_by,checked_date,note FROM evidence WHERE threat_id=? ORDER BY id", (t["id"],))]
                for e in t["evidence"]:
                    e["checked"] = bool(e["checked"])
                t["mitigations"] = [dict(r) for r in db.execute("SELECT text,reference_id,note FROM mitigations WHERE threat_id=? ORDER BY id", (t["id"],))]
                t["score"], t["band"] = priority(t["feasibility"], t["impact"])
                if filters.get("component") and filters["component"] not in t["components"]:
                    continue
                if any(filters.get(k) and filters[k] != t[k] for k in ["stride", "band", "confidence", "review_status"]):
                    continue
                if filters.get("q") and filters["q"].casefold() not in json.dumps(t, ensure_ascii=False).casefold():
                    continue
                result.append(t)
        return sorted(result, key=lambda t: (t["score"] is None, -(t["score"] or 0), -(t["impact"] or 0), t["id"]))

    def threat(self, tid):
        for t in self.threats():
            if t["id"] == tid:
                return t
        raise KeyError(tid)

    def save_threat(self, data, new=False):
        t = validate_threat(data, {x["id"] for x in self.references()})
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            previous = db.execute("SELECT revision FROM threats WHERE id=?", (t["id"],)).fetchone()
            if new and previous:
                raise Conflict("This threat ID already exists")
            if not new and not previous:
                raise KeyError(t["id"])
            revision = 1 if new else previous["revision"] + 1
            if not new and data.get("revision") != previous["revision"]:
                raise Conflict("This record changed. Reload it before saving")
            self._write_threat(db, t, revision)
            for entity in t["components"] + t["flows"]:
                db.execute("UPDATE coverage SET status='Pending',reason='A matching candidate was added or changed. Review this cell again.',reviewer='',review_date='',revision=revision+1 WHERE entity=? AND stride=? AND status='No applicable threat'", (entity, t["stride"]))
            if not new:
                # An edited threat changes the basis of earlier coverage decisions.
                for row in db.execute("SELECT entity,stride,threat_ids FROM coverage WHERE status='Linked'").fetchall():
                    if t["id"] in json.loads(row["threat_ids"]):
                        db.execute("UPDATE coverage SET status='Pending',reason='Linked threat changed. Review this cell again.',reviewer='',review_date='',revision=revision+1 WHERE entity=? AND stride=?", (row["entity"], row["stride"]))
            db.execute("UPDATE scope_reviews SET status='Pending',reason='Catalogue changed. Review scope again.',reviewer='',review_date='',revision=revision+1 WHERE status='Reviewed'")
            self._audit(db, "create_threat" if new else "edit_threat", t["id"], f"Revision {revision}. Previous independent ratings are retained under their original revision.")
        return self.threat(t["id"])

    def coverage(self):
        threats = self.threats()
        with self.connection() as db:
            cells = [dict(r) for r in db.execute("SELECT * FROM coverage ORDER BY entity,stride")]
            scope = [dict(r) for r in db.execute("SELECT * FROM scope_reviews ORDER BY entity")]
        for cell in cells:
            cell["threat_ids"] = json.loads(cell["threat_ids"])
            cell["candidates"] = [t["id"] for t in threats if cell["entity"] in t["components"] + t["flows"] and t["stride"] == cell["stride"]]
        return {"cells": cells, "scope_reviews": scope, "total": 66,
                "completed": sum(c["status"] != "Pending" for c in cells),
                "scope_completed": sum(s["status"] == "Reviewed" for s in scope)}

    def save_coverage(self, data):
        entity, stride = data.get("entity"), data.get("stride")
        status = data.get("status")
        if status not in ["Pending", "Linked", "No applicable threat"]:
            raise Invalid("Unknown worksheet outcome")
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            old = db.execute("SELECT * FROM coverage WHERE entity=? AND stride=?", (entity, stride)).fetchone()
            if not old:
                raise Invalid("Unknown worksheet cell")
            if data.get("revision") != old["revision"]:
                raise Conflict("This cell changed. Reload the worksheet")
            ids = data.get("threat_ids", [])
            if not isinstance(ids, list) or any(not isinstance(x, str) for x in ids):
                raise Invalid("Threat IDs must be a list")
            if status == "Linked":
                if not ids or len(ids) != len(set(ids)):
                    raise Invalid("Choose at least one distinct threat")
                for tid in ids:
                    row = db.execute("SELECT stride FROM threats WHERE id=?", (tid,)).fetchone()
                    mapping = db.execute("SELECT 1 FROM mappings WHERE threat_id=? AND ref_id=? AND kind IN ('components','flows')", (tid, entity)).fetchone()
                    if not row or row["stride"] != stride or not mapping:
                        raise Invalid("Linked threats must match this entity and STRIDE category")
            else:
                ids = []
            reason = required_text(data.get("reason"), "Review reason") if status != "Pending" else str(data.get("reason", ""))
            reviewer = required_text(data.get("reviewer"), "reviewer") if status != "Pending" else ""
            review_date = valid_date(data.get("review_date")) if status != "Pending" else ""
            db.execute("UPDATE coverage SET status=?,threat_ids=?,reason=?,reviewer=?,review_date=?,revision=revision+1 WHERE entity=? AND stride=?",
                       (status, json.dumps(ids), reason, reviewer, review_date, entity, stride))
            self._audit(db, "coverage", f"{entity}:{stride}", status)
        return self.coverage()

    def save_scope_review(self, data):
        entity = data.get("entity")
        if data.get("status") not in ["Pending", "Reviewed"]:
            raise Invalid("Unknown scope review status")
        reviewed = data["status"] == "Reviewed"
        reason = required_text(data.get("reason"), "scope review reason") if reviewed else ""
        reviewer = required_text(data.get("reviewer"), "reviewer") if reviewed else ""
        review_date = valid_date(data.get("review_date")) if reviewed else ""
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            old = db.execute("SELECT revision FROM scope_reviews WHERE entity=?", (entity,)).fetchone()
            if not old:
                raise Invalid("Unknown asset or trust boundary")
            if old["revision"] != data.get("revision"):
                raise Conflict("This scope review changed. Reload the worksheet")
            db.execute("UPDATE scope_reviews SET status=?,reason=?,reviewer=?,review_date=?,revision=revision+1 WHERE entity=?", (data["status"], reason, reviewer, review_date, entity))
            self._audit(db, "scope_review", entity, data["status"])
        return self.coverage()

    def submit_rating(self, data):
        if data.get("rater") not in ["John", "Marius"]:
            raise Invalid("Choose John or Marius")
        f, i = rating(data.get("feasibility"), "feasibility"), rating(data.get("impact"), "impact")
        fr, ir = required_text(data.get("feasibility_reason"), "feasibility reason"), required_text(data.get("impact_reason"), "impact reason")
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            t = db.execute("SELECT revision FROM threats WHERE id=?", (data.get("threat_id"),)).fetchone()
            if not t:
                raise KeyError(data.get("threat_id"))
            if data.get("revision") != t["revision"]:
                raise Conflict("The threat changed. Read the current record before rating it")
            try:
                db.execute("INSERT INTO ratings VALUES (?,?,?,?,?,?,?,?)", (data["threat_id"], t["revision"], data["rater"], f, i, fr, ir, now()))
            except sqlite3.IntegrityError:
                raise Conflict("Initial ratings are locked. Discuss differences in the consensus form")
            self._audit(db, "initial_rating", data["threat_id"], data["rater"])

    def consistency(self, rater):
        if rater not in ["John", "Marius"]:
            raise Invalid("Choose John or Marius")
        rows = []
        with self.connection() as db:
            for t in self.threats():
                ratings = [dict(r) for r in db.execute("SELECT * FROM ratings WHERE threat_id=? AND threat_revision=? ORDER BY rater", (t["id"], t["revision"]))]
                paired = len(ratings) == 2
                cons = db.execute("SELECT * FROM consensus WHERE threat_id=? AND threat_revision=?", (t["id"], t["revision"])).fetchone()
                rows.append({"id": t["id"], "title": t["title"], "revision": t["revision"], "paired": paired,
                             "submitted_by": [r["rater"] for r in ratings],
                             "ratings": ratings if paired else [r for r in ratings if r["rater"] == rater],
                             "consensus": dict(cons) if cons else None})
        pairs = [r for r in rows if r["paired"]]
        n = len(pairs)
        fa = sum(r["ratings"][0]["feasibility"] == r["ratings"][1]["feasibility"] for r in pairs)
        ia = sum(r["ratings"][0]["impact"] == r["ratings"][1]["impact"] for r in pairs)
        return {"rater": rater, "records": rows, "pairs": n, "target_min": 10, "target_max": 15,
                "feasibility_agreements": fa, "impact_agreements": ia,
                "feasibility_percent": round(100 * fa / n, 1) if n else None,
                "impact_percent": round(100 * ia / n, 1) if n else None,
                "resolved": sum(bool(r["consensus"]) and r["consensus"]["outcome"] == "Agreed" for r in pairs),
                "escalated": sum(bool(r["consensus"]) and r["consensus"]["outcome"] == "Escalated" for r in pairs)}

    def save_consensus(self, data):
        outcome = data.get("outcome")
        if outcome not in ["Agreed", "Escalated"]:
            raise Invalid("Choose Agreed or Escalated")
        reason, criterion, who = [required_text(data.get(k), k) for k in ["reason", "criterion", "recorded_by"]]
        f = rating(data.get("feasibility"), "feasibility") if outcome == "Agreed" else None
        i = rating(data.get("impact"), "impact") if outcome == "Agreed" else None
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            t = db.execute("SELECT revision FROM threats WHERE id=?", (data.get("threat_id"),)).fetchone()
            if not t or data.get("revision") != t["revision"]:
                raise Conflict("Threat revision changed")
            count = db.execute("SELECT COUNT(*) FROM ratings WHERE threat_id=? AND threat_revision=?", (data["threat_id"], t["revision"])).fetchone()[0]
            if count != 2:
                raise Invalid("Both initial ratings are required before discussion")
            db.execute("INSERT INTO consensus VALUES (?,?,?,?,?,?,?,?,?) ON CONFLICT(threat_id,threat_revision) DO UPDATE SET outcome=excluded.outcome,feasibility=excluded.feasibility,impact=excluded.impact,reason=excluded.reason,criterion=excluded.criterion,recorded_by=excluded.recorded_by,created_at=excluded.created_at",
                       (data["threat_id"], t["revision"], outcome, f, i, reason, criterion, who, now()))
            self._audit(db, "consensus", data["threat_id"], outcome)

    def snapshot(self):
        # Use SQLite backup to make a consistent copy even while another request writes.
        with self.connection() as db:
            target = sqlite3.connect(":memory:")
            db.backup(target)
            raw = target.serialize()
            target.close()
        return raw

    def evaluation_export(self):
        with self.connection() as db:
            ratings = [dict(r) for r in db.execute("SELECT * FROM ratings ORDER BY threat_id,threat_revision,rater")]
            consensus = [dict(r) for r in db.execute("SELECT * FROM consensus ORDER BY threat_id,threat_revision")]
            audit = [dict(r) for r in db.execute("SELECT * FROM audit ORDER BY id")]
        return {"exported_at": now(), "coverage": self.coverage(), "initial_ratings": ratings,
                "consensus": consensus, "audit": audit,
                "note": "Raw export includes both raters. Use only after independent submissions. No results are fabricated."}
