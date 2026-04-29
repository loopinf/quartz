#!/usr/bin/env python3
"""Local helper that accepts Hermes stage-3 discussion requests from the
Quartz site, creates a dedicated Discord thread per request, and writes an
auditable markdown record into content/market-intel/hermes-inbox/.

Stage-3 behavior:
- POST /api/hermes-request with page context + request_text.
- Helper posts a starter message in the configured Discord parent channel,
  creates a public thread from that starter, and posts a kickoff message
  inside the new thread with full page context + the user's request.
- Helper writes one markdown audit file per request, including the resulting
  thread id / url.

Bind:
- 127.0.0.1 only. No auth.

Run:
    python3 scripts/hermes_inbox_server.py
Optional env:
    HERMES_INBOX_PORT (default 8765)
    HERMES_INBOX_DIR  (default <repo>/content/market-intel/hermes-inbox)
    HERMES_DISCORD_PARENT_CHANNEL (default 1493792291150762115)
    HERMES_ENV_FILE   (default ~/.hermes/.env, used to read DISCORD_BOT_TOKEN)
    DISCORD_BOT_TOKEN (overrides .env if set)
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INBOX = REPO_ROOT / "content" / "market-intel" / "hermes-inbox"
INBOX_DIR = Path(os.environ.get("HERMES_INBOX_DIR", str(DEFAULT_INBOX)))
PORT = int(os.environ.get("HERMES_INBOX_PORT", "8765"))

DEFAULT_PARENT_CHANNEL = "1493792291150762115"
PARENT_CHANNEL_ID = os.environ.get(
    "HERMES_DISCORD_PARENT_CHANNEL", DEFAULT_PARENT_CHANNEL
).strip()

HERMES_ENV_FILE = Path(
    os.environ.get("HERMES_ENV_FILE", str(Path.home() / ".hermes" / ".env"))
)

ALLOWED_ORIGINS = {
    "http://127.0.0.1:8081",
    "http://localhost:8081",
}

SLUG_RE = re.compile(r"[^a-zA-Z0-9._-]+")
DISCORD_API = "https://discord.com/api/v10"


def slugify(value: str, fallback: str) -> str:
    cleaned = SLUG_RE.sub("-", value or "").strip("-")
    return (cleaned or fallback)[:60]


def load_discord_token() -> str | None:
    token = os.environ.get("DISCORD_BOT_TOKEN")
    if token:
        return token.strip()
    if not HERMES_ENV_FILE.exists():
        return None
    try:
        for raw in HERMES_ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            if key.strip() != "DISCORD_BOT_TOKEN":
                continue
            val = val.strip()
            if (val.startswith('"') and val.endswith('"')) or (
                val.startswith("'") and val.endswith("'")
            ):
                val = val[1:-1]
            return val or None
    except OSError:
        return None
    return None


def yaml_escape(value: str) -> str:
    if value is None:
        return '""'
    if "\n" in value or len(value) > 120:
        body = value.replace("\r\n", "\n").rstrip()
        indented = "\n".join("  " + line for line in body.split("\n"))
        return "|\n" + indented
    return json.dumps(value, ensure_ascii=False)


def build_markdown(req: dict) -> str:
    fields = [
        ("request_id", req["request_id"]),
        ("created_at", req["created_at"]),
        ("source_page_title", req.get("source_page_title", "")),
        ("source_page_path", req.get("source_page_path", "")),
        ("source_page_url", req.get("source_page_url", "")),
        ("entity_type", req.get("entity_type", "")),
        ("entity_name", req.get("entity_name", "")),
        ("request_status", req.get("request_status", "queued")),
        ("discord_parent_channel_id", req.get("discord_parent_channel_id", "")),
        ("discord_thread_id", req.get("discord_thread_id", "")),
        ("discord_thread_name", req.get("discord_thread_name", "")),
        ("discord_thread_url", req.get("discord_thread_url", "")),
    ]
    lines = ["---"]
    for key, val in fields:
        lines.append(f"{key}: {yaml_escape(str(val))}")
    lines.append("request_text: " + yaml_escape(req.get("request_text", "")))
    if req.get("error"):
        lines.append("error: " + yaml_escape(str(req["error"])))
    lines.append("---")
    lines.append("")
    lines.append("# Hermes discussion request")
    lines.append("")
    lines.append(
        f"- **page**: {req.get('source_page_title', '')} (`{req.get('source_page_path', '')}`)"
    )
    lines.append(f"- **entity**: {req.get('entity_type', '')} / {req.get('entity_name', '')}")
    lines.append(f"- **status**: {req.get('request_status', 'queued')}")
    if req.get("discord_thread_url"):
        lines.append(f"- **thread**: {req['discord_thread_url']}")
    lines.append("")
    lines.append("## Request")
    lines.append("")
    lines.append(req.get("request_text", "").strip() or "_(empty)_")
    lines.append("")
    return "\n".join(lines)


def build_kickoff_message(record: dict) -> str:
    parts = [
        "**Hermes discussion request**",
        f"- request_id: `{record['request_id']}`",
        f"- page: {record.get('source_page_title') or '(unknown)'}",
    ]
    if record.get("source_page_url"):
        parts.append(f"- url: <{record['source_page_url']}>")
    if record.get("entity_type") or record.get("entity_name"):
        parts.append(
            f"- entity: {record.get('entity_type') or '?'} / {record.get('entity_name') or '?'}"
        )
    parts.append("")
    parts.append("**Request**")
    parts.append(record.get("request_text", "").strip() or "_(empty)_")
    msg = "\n".join(parts)
    # Discord message limit is 2000 chars.
    if len(msg) > 1900:
        msg = msg[:1890] + "\n…(truncated)"
    return msg


def discord_request(method: str, path: str, token: str, body: dict | None) -> dict:
    url = DISCORD_API + path
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bot {token}")
    req.add_header("User-Agent", "hermes-inbox/1.0 (+local)")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read()
            if not raw:
                return {}
            return json.loads(raw.decode("utf-8"))
    except urllib.error.HTTPError as exc:
        try:
            detail = exc.read().decode("utf-8", errors="replace")
        except Exception:
            detail = ""
        raise RuntimeError(f"discord {method} {path} failed: {exc.code} {detail[:300]}")
    except urllib.error.URLError as exc:
        raise RuntimeError(f"discord {method} {path} network error: {exc}")


def create_discord_thread(token: str, parent_channel_id: str, record: dict) -> dict:
    thread_name = (
        f"{record.get('source_page_title') or record.get('entity_name') or 'hermes'} · "
        f"{record['request_id']}"
    )[:95]

    starter_content = (
        f"🧵 Hermes thread for **{record.get('source_page_title') or record.get('entity_name') or 'page'}** "
        f"(request `{record['request_id']}`)"
    )
    starter = discord_request(
        "POST",
        f"/channels/{parent_channel_id}/messages",
        token,
        {"content": starter_content[:1900]},
    )
    starter_id = starter.get("id")
    if not starter_id:
        raise RuntimeError("discord starter message missing id")

    thread = discord_request(
        "POST",
        f"/channels/{parent_channel_id}/messages/{starter_id}/threads",
        token,
        {"name": thread_name, "auto_archive_duration": 1440},
    )
    thread_id = thread.get("id")
    if not thread_id:
        raise RuntimeError("discord thread missing id")

    discord_request(
        "POST",
        f"/channels/{thread_id}/messages",
        token,
        {"content": build_kickoff_message(record)},
    )

    guild_id = thread.get("guild_id") or starter.get("guild_id") or ""
    url = (
        f"https://discord.com/channels/{guild_id}/{thread_id}"
        if guild_id
        else f"https://discord.com/channels/@me/{thread_id}"
    )
    return {
        "thread_id": str(thread_id),
        "thread_name": thread.get("name") or thread_name,
        "thread_url": url,
        "starter_message_id": str(starter_id),
    }


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):  # quieter access log
        sys.stderr.write("[hermes-inbox] " + (fmt % args) + "\n")

    def _cors(self, origin: str | None):
        allow = origin if origin in ALLOWED_ORIGINS else "http://127.0.0.1:8081"
        self.send_header("Access-Control-Allow-Origin", allow)
        self.send_header("Vary", "Origin")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors(self.headers.get("Origin"))
        self.end_headers()

    def do_GET(self):
        if self.path != "/health":
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)
        self._cors(self.headers.get("Origin"))
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        body = {
            "ok": True,
            "inbox": str(INBOX_DIR),
            "discord_parent_channel_id": PARENT_CHANNEL_ID,
            "discord_token_loaded": bool(load_discord_token()),
        }
        self.wfile.write(json.dumps(body).encode())

    def do_POST(self):
        if self.path != "/api/hermes-request":
            self.send_response(404)
            self.end_headers()
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length) if length > 0 else b"{}"
            payload = json.loads(raw.decode("utf-8") or "{}")
        except (ValueError, json.JSONDecodeError) as exc:
            return self._json(400, {"ok": False, "error": f"bad json: {exc}"})

        text = (payload.get("request_text") or "").strip()
        if not text:
            return self._json(400, {"ok": False, "error": "request_text is required"})
        if len(text) > 8000:
            return self._json(400, {"ok": False, "error": "request_text too long (>8000 chars)"})

        token = load_discord_token()
        if not token:
            return self._json(
                500,
                {
                    "ok": False,
                    "error": "DISCORD_BOT_TOKEN not configured (set env or ~/.hermes/.env)",
                },
            )
        if not PARENT_CHANNEL_ID:
            return self._json(
                500, {"ok": False, "error": "HERMES_DISCORD_PARENT_CHANNEL not set"}
            )

        now = datetime.now(timezone.utc)
        request_id = now.strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:6]
        record = {
            "request_id": request_id,
            "created_at": now.isoformat(timespec="seconds").replace("+00:00", "Z"),
            "source_page_title": str(payload.get("source_page_title") or "").strip(),
            "source_page_path": str(payload.get("source_page_path") or "").strip(),
            "source_page_url": str(payload.get("source_page_url") or "").strip(),
            "entity_type": str(payload.get("entity_type") or "").strip(),
            "entity_name": str(payload.get("entity_name") or "").strip(),
            "request_text": text,
            "request_status": "pending",
            "discord_parent_channel_id": PARENT_CHANNEL_ID,
            "discord_thread_id": "",
            "discord_thread_name": "",
            "discord_thread_url": "",
        }

        thread_info: dict | None = None
        error_msg = ""
        try:
            thread_info = create_discord_thread(token, PARENT_CHANNEL_ID, record)
            record["discord_thread_id"] = thread_info["thread_id"]
            record["discord_thread_name"] = thread_info["thread_name"]
            record["discord_thread_url"] = thread_info["thread_url"]
            record["request_status"] = "thread_created"
        except Exception as exc:
            error_msg = str(exc)
            record["request_status"] = "failed"
            record["error"] = error_msg

        INBOX_DIR.mkdir(parents=True, exist_ok=True)
        slug = slugify(record["source_page_title"] or record["entity_name"], "page")
        filename = f"{request_id}_{slug}.md"
        target = INBOX_DIR / filename
        try:
            target.write_text(build_markdown(record), encoding="utf-8")
        except OSError as exc:
            if not error_msg:
                error_msg = f"failed to write audit file: {exc}"

        try:
            rel = str(target.relative_to(REPO_ROOT))
        except ValueError:
            rel = str(target)

        if thread_info is None:
            return self._json(
                502,
                {
                    "ok": False,
                    "error": error_msg or "discord thread creation failed",
                    "request_id": request_id,
                    "path": rel,
                },
            )

        self._json(
            200,
            {
                "ok": True,
                "request_id": request_id,
                "path": rel,
                "absolute_path": str(target),
                "discord_thread_id": record["discord_thread_id"],
                "discord_thread_url": record["discord_thread_url"],
                "discord_thread_name": record["discord_thread_name"],
            },
        )

    def _json(self, status: int, body: dict):
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self._cors(self.headers.get("Origin"))
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def main():
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    token_loaded = bool(load_discord_token())
    print(
        f"[hermes-inbox] listening on http://127.0.0.1:{PORT} -> {INBOX_DIR}",
        flush=True,
    )
    print(
        f"[hermes-inbox] discord parent_channel={PARENT_CHANNEL_ID} token_loaded={token_loaded}",
        flush=True,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()


if __name__ == "__main__":
    main()
