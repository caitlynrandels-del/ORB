from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class OroboroState:
    marker: str = "AWAKENING"
    current_input: Optional[Any] = None
    current_meaning: Optional[Dict[str, Any]] = None
    last_action: Optional[Dict[str, Any]] = None

    def snapshot(self) -> Dict[str, Any]:
        return {
            "marker": self.marker,
            "current_input": self.current_input,
            "current_meaning": self.current_meaning,
            "last_action": self.last_action,
        }
