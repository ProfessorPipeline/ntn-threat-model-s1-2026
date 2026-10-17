PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS architecture (
    kind TEXT NOT NULL, id TEXT NOT NULL, name TEXT NOT NULL, PRIMARY KEY(kind,id)
);
CREATE TABLE IF NOT EXISTS sources (
    id TEXT PRIMARY KEY, citation TEXT NOT NULL, kind TEXT NOT NULL,
    doi TEXT NOT NULL DEFAULT '', note TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS threats (
    id TEXT PRIMARY KEY, scenario TEXT NOT NULL CHECK(scenario='S1'),
    title TEXT NOT NULL, stride TEXT NOT NULL, description TEXT NOT NULL,
    actor TEXT NOT NULL, conditions TEXT NOT NULL, controls TEXT NOT NULL,
    consequence TEXT NOT NULL, feasibility INTEGER CHECK(feasibility BETWEEN 1 AND 4),
    impact INTEGER CHECK(impact BETWEEN 1 AND 4), feasibility_reason TEXT NOT NULL,
    impact_reason TEXT NOT NULL, confidence TEXT NOT NULL,
    confidence_reason TEXT NOT NULL, review_status TEXT NOT NULL,
    reviewer TEXT NOT NULL, review_date TEXT NOT NULL, origin TEXT NOT NULL,
    limitations TEXT NOT NULL, revision INTEGER NOT NULL DEFAULT 1,
    updated_at TEXT NOT NULL, CHECK((feasibility IS NULL) = (impact IS NULL))
);
CREATE TABLE IF NOT EXISTS mappings (
    threat_id TEXT NOT NULL REFERENCES threats(id) ON DELETE CASCADE,
    kind TEXT NOT NULL, ref_id TEXT NOT NULL,
    PRIMARY KEY(threat_id,kind,ref_id),
    FOREIGN KEY(kind,ref_id) REFERENCES architecture(kind,id)
);
CREATE TABLE IF NOT EXISTS evidence (
    id INTEGER PRIMARY KEY, threat_id TEXT NOT NULL REFERENCES threats(id) ON DELETE CASCADE,
    reference_id TEXT REFERENCES sources(id), basis TEXT NOT NULL,
    locator TEXT NOT NULL, checked INTEGER NOT NULL, checked_by TEXT NOT NULL,
    checked_date TEXT NOT NULL, note TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS mitigations (
    id INTEGER PRIMARY KEY, threat_id TEXT NOT NULL REFERENCES threats(id) ON DELETE CASCADE,
    text TEXT NOT NULL, reference_id TEXT REFERENCES sources(id), note TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS coverage (
    entity TEXT NOT NULL, stride TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'Pending',
    threat_ids TEXT NOT NULL DEFAULT '[]', reason TEXT NOT NULL DEFAULT '',
    reviewer TEXT NOT NULL DEFAULT '', review_date TEXT NOT NULL DEFAULT '',
    revision INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY(entity,stride)
);
CREATE TABLE IF NOT EXISTS scope_reviews (
    entity TEXT PRIMARY KEY, status TEXT NOT NULL DEFAULT 'Pending',
    reason TEXT NOT NULL DEFAULT '', reviewer TEXT NOT NULL DEFAULT '',
    review_date TEXT NOT NULL DEFAULT '', revision INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS ratings (
    threat_id TEXT NOT NULL REFERENCES threats(id), threat_revision INTEGER NOT NULL,
    rater TEXT NOT NULL CHECK(rater IN ('John','Marius')),
    feasibility INTEGER NOT NULL CHECK(feasibility BETWEEN 1 AND 4),
    impact INTEGER NOT NULL CHECK(impact BETWEEN 1 AND 4),
    feasibility_reason TEXT NOT NULL, impact_reason TEXT NOT NULL,
    created_at TEXT NOT NULL,
    PRIMARY KEY(threat_id,threat_revision,rater)
);
CREATE TABLE IF NOT EXISTS consensus (
    threat_id TEXT NOT NULL REFERENCES threats(id), threat_revision INTEGER NOT NULL,
    outcome TEXT NOT NULL CHECK(outcome IN ('Agreed','Escalated')),
    feasibility INTEGER CHECK(feasibility BETWEEN 1 AND 4),
    impact INTEGER CHECK(impact BETWEEN 1 AND 4),
    reason TEXT NOT NULL, criterion TEXT NOT NULL,
    recorded_by TEXT NOT NULL, created_at TEXT NOT NULL,
    PRIMARY KEY(threat_id,threat_revision)
);
CREATE TABLE IF NOT EXISTS audit (
    id INTEGER PRIMARY KEY, action TEXT NOT NULL, target TEXT NOT NULL,
    at TEXT NOT NULL, detail TEXT NOT NULL
);
