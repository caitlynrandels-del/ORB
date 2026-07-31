from __future__ import annotations

from typing import Any, Dict, Optional


class MidiInputBridge:
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

    def interpret_note(self, note: Optional[int]) -> str:
        if note is None:
            return "silence"
        if note % 12 == 0:
            return "origin"
        if note % 12 == 4:
            return "journey"
        if note % 12 == 7:
            return "echo"
        return "signal"
