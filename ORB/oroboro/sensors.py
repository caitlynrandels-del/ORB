from __future__ import annotations

from typing import Any, Dict, Optional


class SensorBridge:
    def __init__(self) -> None:
        self.sources: Dict[str, Any] = {}

    def register(self, name: str, source: Any) -> None:
        self.sources[name] = source

    def poll(self, source_name: str) -> Optional[Dict[str, Any]]:
        source = self.sources.get(source_name)
        if source is None:
            return None
        if hasattr(source, "get"):
            return dict(source.get("value", source))
        return {"value": source}

    def poll_all(self) -> Dict[str, Dict[str, Any]]:
        return {name: self.poll(name) or {"value": None} for name in self.sources}
