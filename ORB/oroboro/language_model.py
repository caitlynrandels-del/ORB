from __future__ import annotations

from typing import Any, Dict, Optional


class LanguageModel:
    def __init__(self) -> None:
        self.name = "heuristic-language-model"

    def interpret(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        source = context.get("source", "unknown") if context else "unknown"
        raw_text = str(input_data).strip().lower()

        meaning = {
            "raw": input_data,
            "concept": raw_text or "unknown",
            "intent": "observe",
            "source": source,
            "confidence": 0.7,
            "entities": [],
            "action_hint": "observe",
            "priority": "normal",
        }

        if not raw_text:
            meaning["intent"] = "idle"
            meaning["action_hint"] = "wait"
            return meaning

        if "artifact" in raw_text or "discover" in raw_text or "explore" in raw_text or "find" in raw_text:
            meaning["intent"] = "discover"
            meaning["action_hint"] = "seek artifact"
            meaning["priority"] = "high"
            meaning["entities"].append("Artifact")

        if "world" in raw_text or "environment" in raw_text:
            meaning["entities"].append("World")

        if "player" in raw_text or "self" in raw_text:
            meaning["entities"].append("Player")

        if source == "midi":
            meaning["intent"] = "resonate"
            meaning["action_hint"] = "let the note shape the next meaning"
            meaning["priority"] = "medium"

        if source == "pygame":
            meaning["intent"] = "track"
            meaning["action_hint"] = "follow the signal through the exploration space"
            meaning["priority"] = "high"

        if "remember" in raw_text:
            meaning["intent"] = "remember"
            meaning["action_hint"] = "stash the trace in memory"
            meaning["priority"] = "medium"

        if "note" in raw_text or "midi" in raw_text:
            meaning["entities"].append("Midi")

        if not meaning["entities"]:
            meaning["entities"] = ["Unknown"]

        return meaning
