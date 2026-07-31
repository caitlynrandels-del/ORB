from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock
from typing import Any
from urllib.parse import urlparse

from core.oroboro_mind import create_engine


WORKSPACE_ROOT = Path(__file__).resolve().parent
OROBORO_ROOT = WORKSPACE_ROOT.parent / "Oroboro"
if OROBORO_ROOT.exists() and str(OROBORO_ROOT) not in sys.path:
    sys.path.insert(0, str(OROBORO_ROOT))

try:
    from UpgradeModule import OroboroCore, _try_create_orb_core_engine  # type: ignore
except (ModuleNotFoundError, ImportError):
    OroboroCore = None  # type: ignore[assignment]
    _try_create_orb_core_engine = None  # type: ignore[assignment]


ENGINE = create_engine()
LOCK = Lock()
SHARED_EVENTS: list[dict[str, Any]] = []

if OroboroCore is not None and _try_create_orb_core_engine is not None:
    ADAPTIVE_CORE: Any | None = OroboroCore(orb_core_engine=_try_create_orb_core_engine())
else:
    ADAPTIVE_CORE = None


def _json_bytes(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, ensure_ascii=True).encode("utf-8")


def _record_event(event: dict[str, Any]) -> None:
    event_copy = dict(event)
    event_copy["timestamp"] = datetime.now(UTC).isoformat()
    SHARED_EVENTS.append(event_copy)
    if len(SHARED_EVENTS) > 200:
        del SHARED_EVENTS[:-200]


def _build_shared_state() -> dict[str, Any]:
    adaptive_graph = None
    adaptive_memory = None
    if ADAPTIVE_CORE is not None:
        adaptive_graph = ADAPTIVE_CORE.state_graph.snapshot()
        adaptive_memory = ADAPTIVE_CORE.memory.summary()

    return {
        "engine_state": ENGINE.state.snapshot(),
        "engine_memory_size": ENGINE.memory.size(),
        "adaptive_available": ADAPTIVE_CORE is not None,
        "adaptive_state_graph": adaptive_graph,
        "adaptive_memory": adaptive_memory,
        "recent_events": SHARED_EVENTS[-20:],
    }


class OroboroApiHandler(BaseHTTPRequestHandler):
    server_version = "OroboroAPIServer/0.1"

    def _write_json(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        body = _json_bytes(payload)
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self) -> None:
        self._write_json(HTTPStatus.NO_CONTENT, {})

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/health":
            with LOCK:
                payload = {
                    "ok": True,
                    "service": "oroboro-api",
                    "shared": _build_shared_state(),
                }
            self._write_json(HTTPStatus.OK, payload)
            return

        if path == "/api/state":
            with LOCK:
                self._write_json(HTTPStatus.OK, {"ok": True, "shared": _build_shared_state()})
            return

        if path == "/api/memory":
            with LOCK:
                payload = {
                    "ok": True,
                    "memory": ENGINE.memory.snapshot(),
                    "shared": _build_shared_state(),
                }
            self._write_json(HTTPStatus.OK, payload)
            return

        self._write_json(
            HTTPStatus.NOT_FOUND,
            {"ok": False, "error": "Not found", "path": path},
        )

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        if path not in {"/api/loop", "/api/event"}:
            self._write_json(
                HTTPStatus.NOT_FOUND,
                {"ok": False, "error": "Not found", "path": path},
            )
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        if content_length <= 0:
            self._write_json(
                HTTPStatus.BAD_REQUEST,
                {"ok": False, "error": "Request body required"},
            )
            return

        try:
            raw = self.rfile.read(content_length)
            payload = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            self._write_json(
                HTTPStatus.BAD_REQUEST,
                {"ok": False, "error": "Invalid JSON"},
            )
            return

        if path == "/api/loop":
            input_data = payload.get("input")
            source = str(payload.get("source", "api"))
            if input_data is None:
                self._write_json(
                    HTTPStatus.BAD_REQUEST,
                    {"ok": False, "error": "Field 'input' is required"},
                )
                return

            with LOCK:
                result = ENGINE.loop(input_data, source=source)
                adaptive = ADAPTIVE_CORE.process_event(input_data, source=source) if ADAPTIVE_CORE is not None else None
                _record_event(
                    {
                        "type": "loop",
                        "source": source,
                        "input": str(input_data),
                        "intent": result.get("meaning", {}).get("intent", "observe"),
                        "confidence": result.get("meaning", {}).get("confidence", 0.0),
                        "review_mode": result.get("meaning", {}).get("review_mode", "legacy"),
                        "marker": result.get("state", {}).get("marker", "PROCESSING"),
                    }
                )
                shared = _build_shared_state()

            self._write_json(
                HTTPStatus.OK,
                {"ok": True, "result": result, "adaptive": adaptive, "shared": shared},
            )
            return

        event_type = str(payload.get("event", "event"))
        detail = str(payload.get("detail", ""))
        source = str(payload.get("source", "ui"))
        if not detail:
            self._write_json(
                HTTPStatus.BAD_REQUEST,
                {"ok": False, "error": "Field 'detail' is required"},
            )
            return

        synthesized_input = f"{event_type}: {detail}"
        with LOCK:
            result = ENGINE.loop(synthesized_input, source=source)
            adaptive = ADAPTIVE_CORE.process_event(synthesized_input, source=source) if ADAPTIVE_CORE is not None else None
            _record_event(
                {
                    "type": event_type,
                    "source": source,
                    "detail": detail,
                    "intent": result.get("meaning", {}).get("intent", "observe"),
                    "confidence": result.get("meaning", {}).get("confidence", 0.0),
                    "review_mode": result.get("meaning", {}).get("review_mode", "legacy"),
                    "marker": result.get("state", {}).get("marker", "PROCESSING"),
                }
            )
            shared = _build_shared_state()

        self._write_json(
            HTTPStatus.OK,
            {
                "ok": True,
                "accepted": {"event": event_type, "detail": detail, "source": source},
                "result": result,
                "adaptive": adaptive,
                "shared": shared,
            },
        )

    def log_message(self, format: str, *args: Any) -> None:
        return


def run_server(host: str = "127.0.0.1", port: int = 8010) -> None:
    server = ThreadingHTTPServer((host, port), OroboroApiHandler)
    print(f"Oroboro API listening on http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    run_server()
