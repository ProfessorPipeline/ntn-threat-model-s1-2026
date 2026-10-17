"""Local HTTP server and REST API. No external packages or services."""
import csv
import io
import json
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

from .domain import MODEL, Conflict, Invalid
from .repository import Repository

ROOT = Path(__file__).resolve().parent.parent
FILTERS = {"component", "stride", "band", "confidence", "review_status", "q"}
CSV_FIELDS = ["id", "scenario", "title", "description", "stride", "feasibility", "impact", "score", "band",
              "feasibility_reason", "impact_reason", "confidence", "confidence_reason",
              "components", "assets", "flows", "boundaries", "actor", "conditions", "controls",
              "consequence", "evidence", "mitigations", "review_status", "reviewer", "review_date",
              "origin", "limitations", "revision"]


def csv_bytes(threats):
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, fieldnames=CSV_FIELDS)
    writer.writeheader()
    for t in threats:
        row = {}
        for key in CSV_FIELDS:
            value = t[key]
            if isinstance(value, list):
                value = json.dumps(value, ensure_ascii=False)
            if value is None:
                value = ""
            # Neutralise spreadsheet formula injection while retaining stored text in JSON.
            if isinstance(value, str) and value.lstrip().startswith(("=", "+", "-", "@")):
                value = "'" + value
            row[key] = value
        writer.writerow(row)
    return ("\ufeff" + out.getvalue()).encode("utf-8")


def api_description():
    paths = {}
    for route, summary in [("/api/model", "Read the S1 architecture and scoring criteria"),
                           ("/api/references", "List supplied bibliographic entries"),
                           ("/api/threats", "Read ranked threats with optional filters"),
                           ("/api/threats/{id}", "Read one threat with evidence and candidate mitigations")]:
        params = []
        if "{id}" in route:
            params = [{"name": "id", "in": "path", "required": True, "schema": {"type": "string"}}]
        if route == "/api/threats":
            params = [{"name": p, "in": "query", "schema": {"type": "string"}} for p in sorted(FILTERS)]
        paths[route] = {"get": {"operationId": route.replace("/", "_").replace("{id}", "detail"), "summary": summary,
                               "parameters": params, "responses": {"200": {"description": "JSON result"}}}}
    return {"openapi": "3.0.3", "info": {"title": "S1 NTN read-only catalogue API", "version": "1.0.0"}, "paths": paths}


def make_server(db_path, host="127.0.0.1", port=8000):
    repo = Repository(db_path)
    class Handler(BaseHTTPRequestHandler):
        server_version = "NTNPrototype/1.0"

        def log_message(self, fmt, *args):
            print(f"{self.address_string()} {fmt % args}")

        def respond(self, status, content, content_type="application/json; charset=utf-8", filename=None):
            if isinstance(content, (dict, list)):
                content = json.dumps(content, ensure_ascii=False).encode("utf-8")
            elif isinstance(content, str):
                content = content.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'")
            if filename:
                self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
            self.end_headers()
            self.wfile.write(content)

        def route(self):
            host_header = self.headers.get("Host", "")
            hostname = urlsplit("//" + host_header).hostname
            if hostname not in {"127.0.0.1", "localhost", "::1"}:
                raise Invalid("Use localhost or 127.0.0.1 to access this local prototype")
            path = unquote(urlsplit(self.path).path)
            query = parse_qs(urlsplit(self.path).query, keep_blank_values=True)
            if any(len(v) != 1 for v in query.values()):
                raise Invalid("Repeated query parameters are not supported")
            return path, {k: v[0] for k, v in query.items() if v[0]}

        def error(self, exc):
            status = 409 if isinstance(exc, Conflict) else 400 if isinstance(exc, (Invalid, ValueError)) else 404 if isinstance(exc, KeyError) else 500
            message = str(exc) if status != 500 else "Internal error. Check the server terminal."
            if status == 500:
                import traceback
                traceback.print_exc()
            self.respond(status, {"error": message})

        def do_GET(self):
            try:
                path, q = self.route()
                if path == "/api/health":
                    return self.respond(200, {"status": "ok", "scenario": "S1", "llm_required": False, "internet_required": False})
                if path == "/api/model":
                    return self.respond(200, MODEL)
                if path in ["/api/openapi.json", "/openapi.json"]:
                    return self.respond(200, api_description())
                if path == "/api/references":
                    return self.respond(200, repo.references())
                if path == "/api/threats":
                    records = repo.threats(q)
                    return self.respond(200, {"items": records, "count": len(records), "sort": "score descending / impact descending / ID ascending / unscored last"})
                if path == "/api/threats.csv":
                    return self.respond(200, csv_bytes(repo.threats(q)), "text/csv; charset=utf-8", "s1-threats.csv")
                if path.startswith("/api/threats/"):
                    return self.respond(200, repo.threat(path.rsplit("/", 1)[1]))
                if path == "/api/coverage":
                    return self.respond(200, repo.coverage())
                if path == "/api/consistency":
                    if set(q) != {"rater"}:
                        raise Invalid("Supply rater=John or rater=Marius")
                    return self.respond(200, repo.consistency(q["rater"]))
                if path == "/api/evaluation.json":
                    return self.respond(200, repo.evaluation_export(), filename="s1-evaluation.json")
                if path == "/api/catalogue.json":
                    return self.respond(200, {"model": MODEL, "references": repo.references(), "threats": repo.threats()}, filename="s1-catalogue.json")
                if path == "/api/database.sqlite3":
                    return self.respond(200, repo.snapshot(), "application/vnd.sqlite3", "ntn-backup.sqlite3")
                if path.startswith("/api/"):
                    raise KeyError("Unknown API route")
                root = ROOT / "web"
                file = (root / (path.lstrip("/") or "index.html")).resolve()
                if not file.is_relative_to(root) or not file.is_file():
                    raise KeyError("File not found")
                return self.respond(200, file.read_bytes(), mimetypes.guess_type(file)[0] or "application/octet-stream")
            except (BrokenPipeError, ConnectionResetError):
                return
            except Exception as exc:
                self.error(exc)

        def read_body(self):
            origin = self.headers.get("Origin")
            if origin and origin != "http://" + self.headers.get("Host", ""):
                raise Invalid("Cross-origin changes are blocked")
            if self.headers.get("X-NTN-Local") != "1":
                raise Invalid("Local writes require X-NTN-Local: 1")
            if self.headers.get_content_type() != "application/json":
                raise Invalid("Use application/json")
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= 1000000:
                raise Invalid("JSON body must be between 1 byte and 1 MB")
            try:
                body = json.loads(self.rfile.read(size))
            except (json.JSONDecodeError, UnicodeDecodeError):
                raise Invalid("Invalid JSON")
            if not isinstance(body, dict):
                raise Invalid("JSON body must be an object")
            return body

        def do_POST(self):
            self.change("POST")

        def do_PUT(self):
            self.change("PUT")

        def change(self, method):
            try:
                path, q = self.route()
                data = self.read_body()
                if method == "POST" and path == "/api/threats":
                    return self.respond(201, repo.save_threat(data, new=True))
                if method == "PUT" and path.startswith("/api/threats/"):
                    if data.get("id") != path.rsplit("/", 1)[1]:
                        raise Invalid("ID does not match the URL")
                    return self.respond(200, repo.save_threat(data))
                if method == "POST" and path == "/api/coverage":
                    return self.respond(200, repo.save_coverage(data))
                if method == "POST" and path == "/api/scope-reviews":
                    return self.respond(200, repo.save_scope_review(data))
                if method == "POST" and path == "/api/ratings":
                    repo.submit_rating(data)
                    return self.respond(201, {"saved": True, "initial_rating_locked": True})
                if method == "POST" and path == "/api/consensus":
                    repo.save_consensus(data)
                    return self.respond(200, {"saved": True, "catalogue_score_changed": False})
                raise KeyError("Unknown write route")
            except Exception as exc:
                self.error(exc)

    server = ThreadingHTTPServer((host, port), Handler)
    server.daemon_threads = True
    server.repository = repo
    return server
