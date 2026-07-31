from __future__ import annotations

from typing import Any, Dict, Optional


class LanguageInterpreter:
    def __init__(self) -> None:
        self.name = "heuristic-language-model"

    def interpret(self, input_data: Any, source: Optional[str] = None) -> Dict[str, Any]:
        raw_text = str(input_data).strip().lower()
        meaning = {
            "raw": input_data,
            "concept": raw_text or "unknown",
            "intent": "observe",
            "source": source or "unknown",
            "confidence": 0.62,
            "entities": [],
            "action_hint": "observe",
            "priority": "normal",
        }

        if not raw_text:
            meaning["intent"] = "idle"
            meaning["action_hint"] = "wait"
            meaning["confidence"] = 0.2
            return meaning

        if any(word in raw_text for word in ["artifact", "discover", "explore", "find"]):
            meaning["intent"] = "discover"
            meaning["action_hint"] = "seek artifact"
            meaning["priority"] = "high"
            meaning["entities"].append("Artifact")
            meaning["confidence"] += 0.1

        if "world" in raw_text or "environment" in raw_text:
            meaning["entities"].append("World")

        if "player" in raw_text or "self" in raw_text:
            meaning["entities"].append("Player")

        if source == "midi":
            meaning["intent"] = "resonate"
            meaning["action_hint"] = "let the note shape the next meaning"
            meaning["priority"] = "medium"
            meaning["confidence"] += 0.08

        if source == "pygame":
            meaning["intent"] = "track"
            meaning["action_hint"] = "follow the signal through the exploration space"
            meaning["priority"] = "high"
            meaning["confidence"] += 0.07

        if "remember" in raw_text:
            meaning["intent"] = "remember"
            meaning["action_hint"] = "stash the trace in memory"
            meaning["priority"] = "medium"
            meaning["confidence"] += 0.08

        if "block" in raw_text or "risk" in raw_text:
            meaning["intent"] = "stabilize"
            meaning["action_hint"] = "reduce blocker and define mitigation"
            meaning["priority"] = "high"
            meaning["confidence"] += 0.09

        if "kpi" in raw_text or "metric" in raw_text:
            meaning["intent"] = "measure"
            meaning["action_hint"] = "select one KPI and baseline"
            meaning["priority"] = "high"
            meaning["confidence"] += 0.08

        if "owner" in raw_text or "handoff" in raw_text:
            meaning["intent"] = "handoff"
            meaning["action_hint"] = "assign owner and due date"
            meaning["priority"] = "high"
            meaning["confidence"] += 0.08

        if "note" in raw_text or "midi" in raw_text:
            meaning["entities"].append("Midi")

        if not meaning["entities"]:
            meaning["entities"] = ["Unknown"]
            meaning["confidence"] -= 0.08

        if len(raw_text.split()) >= 5:
            meaning["confidence"] += 0.04

        if len(raw_text) > 140:
            meaning["confidence"] -= 0.03

        if "?" in raw_text:
            meaning["confidence"] -= 0.02

        meaning["confidence"] = max(0.05, min(0.98, round(float(meaning["confidence"]), 3)))

        return meaning
