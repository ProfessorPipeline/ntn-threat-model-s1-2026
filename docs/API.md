# Local REST API

Base URL: `http://127.0.0.1:8000`.

All records use scenario S1. JSON responses use UTF-8. Invalid input returns HTTP 400. Missing records return 404. Stale edits and duplicate initial ratings return 409. Errors use an `error` field.

## Read routes

| Method and route | Result |
| --- | --- |
| `GET /api/health` | Local core status and independence from LLM or internet |
| `GET /api/model` | Architecture and scope plus F and I criteria |
| `GET /api/references` | Supplied source register |
| `GET /api/threats` | Ranked records in `items` plus `count` |
| `GET /api/threats/T-02` | One full threat |
| `GET /api/threats.csv` | Filtered CSV with evidence and reasons |
| `GET /api/coverage` | 66 cells and nine scope reviews |
| `GET /api/consistency?rater=John` | Current-revision ratings visible to John and aggregate agreement |
| `GET /api/catalogue.json` | Model and current sources plus full catalogue |
| `GET /api/evaluation.json` | All initial rating history and consensus plus coverage and audit |
| `GET /api/database.sqlite3` | Consistent SQLite backup |
| `GET /api/openapi.json` | Read-only catalogue API description |

The evaluation export contains both raters' data. Use it after both have completed their independent work. This trusted local prototype does not implement identity or access control.

## Filters

`/api/threats` and `/api/threats.csv` accept the same filters. Filters combine using AND.

| Parameter | Examples |
| --- | --- |
| `component` | `C1` through `C6` |
| `stride` | `Tampering` or `Information Disclosure` |
| `band` | `Low` / `Medium` / `High` / `Critical` / `Unscored` |
| `confidence` | `Low` / `Medium` / `High` |
| `review_status` | `Imported` / `Draft` / `Reviewed` |
| `q` | Case-insensitive text search |

Example:

```text
/api/threats?component=C3&stride=Tampering
```

The initial result is T-02 only. CSV returns the same selected IDs.

## Write routes

Writes need `Content-Type: application/json` and `X-NTN-Local: 1`. Browser writes must have the same origin. Hostnames are limited to localhost and loopback addresses.

| Method and route | Purpose |
| --- | --- |
| `POST /api/threats` | Create a threat with a new ID |
| `PUT /api/threats/T-02` | Replace a threat using its current `revision` |
| `POST /api/coverage` | Save one worksheet outcome with current cell revision |
| `POST /api/scope-reviews` | Save one asset or boundary review |
| `POST /api/ratings` | Lock one student's initial rating for a threat revision |
| `POST /api/consensus` | Record an agreed or escalated discussion outcome |

Use the browser forms for normal entry. To script a threat edit first fetch the full object then modify the required fields and send it to the same ID. The database validates mappings and references. A Reviewed record needs reviewer names and a real review date.

Ratings require an integer F and I from 1 to 4 plus both reasons. Threat catalogue ratings may both be null. A partially scored threat is rejected. Checked source support requires a reference and locator plus the checker's name and date.

## Ranking

Compute the priority at read time as F × I. Bands are Low 1–3 and Medium 4–7 plus High 8–11 and Critical 12–16. The matrix and bands are the team's adaptation. Confidence does not enter the product.

Sort scored records by score descending then impact descending then threat ID ascending. Unscored records appear last. Scores cannot be set directly through the API.

## Scoring history

Initial ratings are unique for a threat revision and rater. They cannot be overwritten through this API. Editing a threat increments its revision. Old initial ratings and consensus stay in the evaluation export but no longer enter current-revision agreement percentages.

Consensus never changes the catalogue score automatically. After a joint decision update the catalogue through its editor if appropriate. This starts a new revision and keeps the old comparison as history.

## Optional external consumers

The supplied read-only OpenAPI description covers model and source reads plus catalogue reads. No LLM integration is required or enabled. Do not expose the local write API to an LLM or a public network.
