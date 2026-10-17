# S1 NTN threat model

Open this folder in VS Code. Python 3.11 or later is the only requirement for the core app. No pip install is needed.

## Start on Windows

Open the VS Code terminal in this folder:

```powershell
py -3 run.py
```

If the Python launcher is unavailable:

```powershell
python run.py
```

Then open <http://127.0.0.1:8000> in a browser. You can also double-click `start-windows.bat`.

## Start on macOS or Linux

```sh
python3 run.py
```

The core works offline after Python is installed. It does not call any external API. It does not need Docker or an LLM or OpenWebUI.

If port 8000 is busy:

```sh
python run.py --port 8001
```

Open <http://127.0.0.1:8001>. Stop with Ctrl+C.

## What is built

- SQLite database with a REST API and a browser interface.
- S1 architecture with six components and five flow groups plus four trust boundaries.
- Component and STRIDE filters with ranked threat details and CSV export.
- Attack feasibility × impact using the latest supplied criteria.
- Threat editing with architecture validation and explicit source checks.
- A 66-cell STRIDE review worksheet with separate asset and boundary reviews.
- Independent scoring for John and Marius with locked initial ratings.
- Initial agreement percentages with separate discussion outcomes and escalation notes.
- Database backup and catalogue export plus a portable offline viewer.
- Optional Docker packaging.

The ranking matrix and bands are the team's own adaptation. They are not the matrix used by Ansong et al. Four levels use concrete criteria and avoid a neutral middle value. Priority is qualitative. It is not an attack probability or a measured network risk.

## What the initial data means

The five scored records T-01 to T-05 come from the latest progress update. Their scores and mappings are preserved. T-06 and T-07 are distinct draft candidates from the older plan. They remain unscored because that plan used likelihood rather than attack feasibility. The plan's passive observation example overlaps T-03 and is not counted again.

All imported examples await a new human review in this package. The source material describes work as completed but those claims are not treated as proof of a review of this newly built code or database. No source support is marked checked. Bibliographic entries are copied from the supplied update. The underlying publications were not read during this build.

There are seven distinct candidates. The planned 10–15 record consistency exercise needs at least three more suitable records. No independent student ratings or evaluation outcomes are prefilled.

Read [docs/REQUIREMENTS.md](docs/REQUIREMENTS.md) for the exact source decisions and remaining work.

## First demo

1. Open Architecture and trace both F5 administration paths.
2. Open Ranking method and explain the team-adapted matrix.
3. Open Threat catalogue. Select C3 and Tampering.
4. Open T-02. Show F2 × I4 = 8 plus its assumptions and candidate mitigation.
5. Export CSV. It should contain T-02 only.
6. Reset filters. Open T-03 and show its source support gaps.
7. Open STRIDE coverage and Independent scoring. Show the real current state.

The Demo guide inside the app divides a suggested 20-minute presentation between both students. It is a plan rather than a claim about completed individual work.

## Save your work

All changes persist in `data/ntn.sqlite3`. Restarting the app does not reset them.

Use **Save database** to download a consistent SQLite backup. **Export evaluation** includes initial ratings from both students. Use that export after independent scoring is complete. Keep a backup before importing any data through your own scripts.

To use a saved database without overwriting your current one:

```sh
python run.py --db path/to/ntn-backup.sqlite3 --port 8001
```

To start a separate clean copy for rehearsal:

```sh
python run.py --db data/rehearsal.sqlite3 --port 8001
```

Do not use rehearsal ratings as research results.

## Offline backup

Open `web/backup.html` directly in a browser if the server fails. It is a self-contained read-only snapshot with filtering and CSV export. It cannot record reviews or ratings.

Regenerate it from your current database:

```sh
python scripts/build_backup.py
```

Record a fresh backup demonstration after important changes. See [docs/DEMO.md](docs/DEMO.md).

A silent walkthrough is included at `docs/demo-backup.mp4`. Screenshots and an example filtered CSV are in `docs/`. These show the initial supplied catalogue rather than a completed human evaluation.

## Tests

```sh
python -m unittest discover -s tests -v
```

These checks use temporary databases. They never add example student ratings to your working database.

## Optional Docker

```sh
docker compose up --build
```

Then open <http://127.0.0.1:8000>. Docker Desktop must be running on Windows. The first image build needs an internet connection. Later runs use a named volume for persistent data.

```sh
docker compose down
```

This keeps the named volume. Avoid `docker compose down -v` unless you intend to delete the Docker database. The normal Python setup needs no image download and remains the simplest offline route.

Docker was not available in the build environment. The Python core is the tested route. Test Docker on both students' computers before relying on it for the seminar.

## Folder guide

| Path | Purpose |
| --- | --- |
| `run.py` | Application entry point |
| `ntn/domain.py` | S1 model and validation plus ranking rules |
| `ntn/repository.py` | Database operations and evaluation records |
| `ntn/server.py` | REST routes and static web server |
| `ntn/schema.sql` | SQLite tables and constraints |
| `data/seed.json` | Traceable starting catalogue and references |
| `web/` | Browser interface and offline viewer |
| `tests/` | Standard-library integration tests |
| `scripts/build_backup.py` | Offline snapshot generator |
| `docs/` | Setup support and evaluation templates |
| `evidence/supplied/` | Unchanged input PDFs |

See [docs/API.md](docs/API.md) for endpoints. This is a local research prototype. The role selector is not an account system. Keep it on localhost.
