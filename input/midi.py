from __future__ import annotations

from typing import Any, Dict, Optional


class MidiInput:
    def __init__(self) -> None:
        self.last_message: Optional[Dict[str, Any]] = None

    def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        self.last_message = message
        return {
            "source": "midi",
            "note": message.get("note"),
            "velocity": message.get("velocity"),
            "channel": message.get("channel"),
        }
