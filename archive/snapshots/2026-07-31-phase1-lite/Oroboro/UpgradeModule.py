"""
OROBORO CONTINUOUS UNDERSTANDING LOOP

Demonstrate understanding of Oroboro by adding features where the system:

1. Observes something
2. Creates meaning from it
3. Remembers it
4. Changes future behavior because of it

Continue expanding this behavior over time, but keep implementations reasonable.

Rules:
- Prefer small, complete improvements over large unfinished systems.
- Preserve existing architecture.
- Do not create unnecessary files.
- Integrate with the existing Oroboro Core Loop.

Core Cycle:

PERCEIVE
    ↓
INTERPRET
    ↓
CONNECT
    ↓
REMEMBER
    ↓
ADAPT
    ↓
ACT
    ↓
REFLECT
    ↓
REPEAT


Example Implementation:
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def _try_create_orb_core_engine() -> Any | None:
    """Load the existing ORB core loop when available."""
    try:
        import sys

        root = Path(__file__).resolve().parents[1] / "ORB"
        if root.exists() and str(root) not in sys.path:
            sys.path.insert(0, str(root))

        from core.oroboro_mind import create_engine  # type: ignore

        return create_engine()
    except (ModuleNotFoundError, ImportError):
        return None


@dataclass
class MemoryEvent:
    source: str
    concept: str
    meaning: dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


class OroboroMemory:

    def __init__(self):

        self.experiences: dict[str, list[MemoryEvent]] = {}
        self.timeline: list[MemoryEvent] = []



    def remember(self, key, value):
        event = MemoryEvent(
            source=value.get("source", "unknown"),
            concept=key,
            meaning=value,
        )
        self.experiences.setdefault(key, []).append(event)
        self.timeline.append(event)
        return event



    def recall(self, key):
        history = self.experiences.get(key, [])
        return history[-1] if history else None

    def count(self, key: str) -> int:
        return len(self.experiences.get(key, []))

    def latest(self):
        return self.timeline[-1] if self.timeline else None




class OroboroMind:


    def __init__(self, core_engine: Any | None = None):

        self.memory = OroboroMemory()

        self.behavior: dict[str, str] = {}
        self.core_engine = core_engine
        self.state = "AWAKENING"
        self.last_action = "Observe"



    def perceive(self, observation):

        """
        Receives information from world.
        """

        if isinstance(observation, dict):
            source = str(observation.get("source", "unknown"))
            raw = str(observation.get("value", observation))
        else:
            source = "unknown"
            raw = str(observation)

        return {
            "source": source,
            "raw": raw,
        }



    def create_meaning(self, observation):

        """
        Converts observation into meaning.
        """

        raw_text = observation["raw"].strip().lower()
        meaning = {
            "source": observation["source"],
            "raw": observation["raw"],
            "concept": raw_text or "unknown",
            "importance": "normal",
            "intent": "observe",
            "entities": ["Unknown"],
        }

        if "danger" in raw_text or "threat" in raw_text:

            meaning["importance"] = "high"
            meaning["intent"] = "defend"
            meaning["entities"] = ["Threat"]


        if "discovery" in raw_text or "artifact" in raw_text:

            meaning["importance"] = "special"
            meaning["intent"] = "discover"
            meaning["entities"] = ["Artifact"]

        if "remember" in raw_text:
            meaning["intent"] = "remember"

        return meaning

    def connect(self, meaning):
        """Connect meaning to prior traces for context-aware adaptation."""
        concept = meaning["concept"]
        repeats = self.memory.count(concept)
        link = {
            "concept": concept,
            "seen_before": repeats > 0,
            "repeat_count": repeats,
        }
        return link



    def remember_experience(self, meaning):

        """
        Stores experience for future behavior.
        """

        self.memory.remember(meaning["concept"], meaning)



    def adapt_behavior(self, meaning):

        """
        Future actions are influenced
        by previous experiences.
        """

        concept = meaning["concept"]
        seen_count = self.memory.count(concept)


        if meaning["importance"] == "special":

            self.behavior[concept] = (
                "Investigate similar events"
            )


        elif meaning["importance"] == "high":

            self.behavior[concept] = (
                "Avoid or prepare"
            )

        elif seen_count >= 3:

            self.behavior[concept] = (
                "Promote to routine and respond faster"
            )


        else:

            self.behavior[concept] = (
                "Observe"
            )

        return self.behavior[concept]

    def act(self, meaning):
        concept = meaning["concept"]
        action = self.behavior.get(concept, "Observe")
        self.last_action = action
        return action

    def reflect(self, meaning, link):
        self.state = "REFLECTING"
        return {
            "state": self.state,
            "last_concept": meaning["concept"],
            "repeat_count": link["repeat_count"],
            "memory_size": len(self.memory.timeline),
            "last_action": self.last_action,
        }



    def process(self, observation):

        """
        Complete Oroboro loop.
        """

        perceived = self.perceive(
            observation
        )


        meaning = self.create_meaning(
            perceived
        )

        link = self.connect(
            meaning
        )


        self.remember_experience(
            meaning
        )


        behavior = self.adapt_behavior(
            meaning
        )

        action = self.act(
            meaning
        )

        reflection = self.reflect(
            meaning,
            link
        )

        return {
            "perceived": perceived,
            "meaning": meaning,
            "link": link,
            "behavior": behavior,
            "action": action,
            "reflection": reflection,
        }

    def process_with_core_loop(self, observation, source="upgrade_module"):
        """Run existing ORB core loop first, then adapt this module behavior."""
        if self.core_engine is None:
            return {
                "core": None,
                "upgrade": self.process({"source": source, "value": observation}),
            }

        core_result = self.core_engine.loop(observation, source=source)
        upgrade_result = self.process(
            {
                "source": source,
                "value": core_result["meaning"].get("concept", observation),
            }
        )

        return {
            "core": core_result,
            "upgrade": upgrade_result,
        }




# -------------------------
# Example Usage
# -------------------------


if __name__ == "__main__":
    core_engine = _try_create_orb_core_engine()
    mind = OroboroMind(core_engine=core_engine)

    demo_events = [
        "discovery: ancient artifact",
        "danger: shadow approaching",
        "discovery: ancient artifact",
        "discovery: ancient artifact",
    ]

    for event in demo_events:
        result = mind.process_with_core_loop(event, source="demo")
        print("Event:", event)
        print("Action:", result["upgrade"]["action"])
        print("Reflection:", result["upgrade"]["reflection"])
        print("---")

    print("Behavior Map:", mind.behavior)
