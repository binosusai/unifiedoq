from __future__ import annotations

import json
import secrets
import sqlite3
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "poc.sqlite3"
FRONTEND = ROOT / "frontend"
IDEA_TITLE = 'Unified API key gateway — one key per project that provisions and proxies all third-party tool API keys'
IDEA_CATEGORY = 'money'
USE_CASE = 'api-key-gateway'
PLAN_SUMMARY = 'Create a working proof of concept that demonstrates the core value of `Unified API key gateway — one key per project that provisions and proxies all third-party tool API keys` with the smallest credible interface. Represent the idea as a concrete user workflow. Create one runnable local draft project.'
RESEARCH_SUMMARY = 'Developers manage dozens of API keys across tools; one unified key per project reduces setup friction, centralizes credential management, and lets teams onboard new tools with a single click This idea is on the `money` track, so the primary research lens is commercial opportunity. Unified API key gateway — one key per project that provisions and proxies all third-party tool API keys is worth exploring if it can produce a visible result within one week and a useful proof of concept within one focused session.'


def init_db() -> None:
    with sqlite3.connect(DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS projects (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL UNIQUE,
              api_key TEXT NOT NULL,
              created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS proxy_runs (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              project_id INTEGER REFERENCES projects(id),
              provider TEXT NOT NULL,
              payload TEXT NOT NULL,
              response TEXT NOT NULL,
              created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS runs (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              input TEXT NOT NULL,
              recommendation TEXT NOT NULL,
              created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)


def mock_proxy_response(provider: str, payload: str, project_name: str) -> str:
    return (
        f"[MOCK PROXY] provider={provider} project={project_name} "
        f"signal={RESEARCH_SUMMARY[:120]} payload_echo={payload[:200]}"
    )


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND), **kwargs)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/health":
            self.send_json(
                {
                    "ok": True,
                    "idea": IDEA_TITLE,
                    "category": IDEA_CATEGORY,
                    "use_case": USE_CASE,
                    "plan_summary": PLAN_SUMMARY[:200],
                }
            )
            return
        if path == "/api/projects":
            with sqlite3.connect(DB) as conn:
                rows = conn.execute(
                    "SELECT id, name, api_key, created_at FROM projects ORDER BY created_at DESC"
                ).fetchall()
            self.send_json(
                [{"id": r[0], "name": r[1], "api_key": r[2], "created_at": r[3]} for r in rows]
            )
            return
        super().do_GET()

    def do_POST(self):
        path = urlparse(self.path).path
        length = int(self.headers.get("content-length", "0"))
        body = json.loads(self.rfile.read(length) or b"{}")

        if path == "/api/projects":
            name = str(body.get("name", "")).strip()
            if not name:
                self.send_error(400, "name required")
                return
            api_key = f"pk_{secrets.token_hex(16)}"
            try:
                with sqlite3.connect(DB) as conn:
                    conn.execute(
                        "INSERT INTO projects(name, api_key) VALUES (?, ?)", (name, api_key)
                    )
            except sqlite3.IntegrityError:
                self.send_error(409, "project name already exists")
                return
            self.send_json({"name": name, "api_key": api_key})
            return

        if path == "/api/proxy/mock":
            api_key = str(body.get("api_key", ""))
            provider = str(body.get("provider", "openai"))
            payload = str(body.get("payload", ""))
            with sqlite3.connect(DB) as conn:
                row = conn.execute(
                    "SELECT id, name FROM projects WHERE api_key = ?", (api_key,)
                ).fetchone()
            if not row:
                self.send_error(401, "invalid api_key")
                return
            project_id, project_name = row
            response = mock_proxy_response(provider, payload, project_name)
            with sqlite3.connect(DB) as conn:
                conn.execute(
                    "INSERT INTO proxy_runs(project_id, provider, payload, response) VALUES (?,?,?,?)",
                    (project_id, provider, payload, response),
                )
            self.send_json({"ok": True, "provider": provider, "response": response})
            return

        if path == "/api/run":
            raw = str(body.get("input", ""))
            recommendation = (
                f"POC recommendation for {IDEA_TITLE} ({USE_CASE}): "
                f"plan emphasis -> {PLAN_SUMMARY[:200]} "
                f"research signal -> {RESEARCH_SUMMARY[:180]} "
                f"input reviewed -> {raw[:220]}"
            )
            with sqlite3.connect(DB) as conn:
                conn.execute(
                    "INSERT INTO runs(input, recommendation) VALUES (?, ?)",
                    (raw, recommendation),
                )
            self.send_json({"recommendation": recommendation})
            return

        self.send_error(404)

    def send_json(self, payload):
        data = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def main() -> None:
    init_db()
    server = ThreadingHTTPServer(("127.0.0.1", 8000), Handler)
    print("POC running at http://localhost:8000")
    print("Press Ctrl+C to stop.")
    server.serve_forever()


if __name__ == "__main__":
    main()
