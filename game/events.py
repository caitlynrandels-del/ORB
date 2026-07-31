from __future__ import annotations

from typing import Any, Dict


class EventBus:
    def __init__(self) -> None:
        self.listeners: Dict[str, list[callable]] = {}

    def subscribe(self, event_name: str, callback: callable) -> None:
        self.listeners.setdefault(event_name, []).append(callback)

    def emit(self, event_name: str, payload: Any = None) -> None:
        for callback in self.listeners.get(event_name, []):
            callback(payload)
