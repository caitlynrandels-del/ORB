from __future__ import annotations

from typing import Any, Dict

from core.state import OroboroState
from core.memory import MemoryStore
from core.entity import Entity, EntitySystem
from language.interpreter import LanguageInterpreter


MAX_ITERATIONS = 3
CONFIDENCE_THRESHOLD = 0.78
MIN_PROGRESS = 0.02


class OroboroMind:
    def __init__(self) -> None:
        self.state = OroboroState()
        self.memory = MemoryStore()
        self.entities = EntitySystem()
        self.language = LanguageInterpreter()
        self._bootstrap_entities()

    def _bootstrap_entities(self) -> None:
        self.entities.add_entity(Entity("Player"))
        self.entities.add_entity(Entity("World"))
        self.entities.add_entity(Entity("Artifact"))
        self.entities.add_entity(Entity("Midi"))

    def perceive(self, input_data: Any, source: str = "unknown") -> Dict[str, Any]:
        self.state.current_input = input_data
        return {"source": source, "value": input_data}

    def interpret(self, input_data: Any, source: str = "unknown") -> Dict[str, Any]:
        meaning = self.language.interpret(input_data, source=source)
        self.state.current_meaning = meaning
        return meaning

    def connect(self, meaning: Dict[str, Any], source_name: str = "Player") -> None:
        for entity_name in meaning.get("entities", []):
            entity = self.entities.get_entity(entity_name)
            if entity is None:
                entity = self.entities.add_entity(Entity(entity_name))
            self.entities.connect_entities(source_name, entity.name, meaning)

    def update_memory(self, meaning: Dict[str, Any], source: str = "unknown") -> None:
        self.memory.remember(meaning, source=source)

    def act(self, meaning: Dict[str, Any]) -> Dict[str, Any]:
        self.state.last_action = {
            "intent": meaning.get("intent", "observe"),
            "action_hint": meaning.get("action_hint", "observe"),
            "priority": meaning.get("priority", "normal"),
        }
        return self.state.last_action

    def reflect(self) -> None:
        if self.state.current_meaning is None:
            self.state.marker = "AWAKENING"
        elif all(entity.resolved for entity in self.entities.entities):
            self.state.marker = "ALL_KNOWN"
        else:
            self.state.marker = "PROCESSING"

    @staticmethod
    def _tokenize_signal(value: Any) -> list[str]:
        text = str(value).strip().lower()
        return [token for token in text.replace(":", " ").replace(",", " ").split() if token]

    @staticmethod
    def _summarize_signal(tokens: list[str], fallback: str = "unknown") -> str:
        if not tokens:
            return fallback
        keep = [token for token in tokens if token.isalpha()][:8]
        return " ".join(keep) if keep else fallback

    def _refine_input(self, input_data: Any, attempt: int) -> Any:
        tokens = self._tokenize_signal(input_data)
        if not tokens:
            return input_data

        # First refinement keeps intent-rich terms, later iterations simplify harder.
        important = [
            token
            for token in tokens
            if token
            in {
                "discover",
                "artifact",
                "remember",
                "blocker",
                "risk",
                "kpi",
                "metric",
                "owner",
                "handoff",
                "decision",
                "pilot",
            }
        ]
        base = important or tokens
        budget = max(3, 8 - attempt)
        return self._summarize_signal(base[:budget], fallback=str(input_data).strip() or "unknown")

    @staticmethod
    def _progress(previous_confidence: float, next_confidence: float) -> float:
        return next_confidence - previous_confidence

    def _looping(self, iteration: int, progress: float) -> bool:
        return iteration >= MAX_ITERATIONS or progress < MIN_PROGRESS

    def _iterative_interpret(self, input_data: Any, source: str) -> dict[str, Any]:
        working_input = input_data
        best_meaning: dict[str, Any] | None = None
        best_confidence = -1.0
        diagnostics: list[dict[str, Any]] = []
        previous_confidence = 0.0

        for iteration in range(1, MAX_ITERATIONS + 1):
            observation = self.perceive(working_input, source=source)
            meaning = self.interpret(observation["value"], source=source)
            confidence = float(meaning.get("confidence", 0.0))
            progress = self._progress(previous_confidence, confidence)
            diagnostics.append(
                {
                    "iteration": iteration,
                    "input": str(working_input),
                    "confidence": round(confidence, 3),
                    "progress": round(progress, 3),
                }
            )

            if confidence > best_confidence:
                best_confidence = confidence
                best_meaning = meaning

            if confidence >= CONFIDENCE_THRESHOLD:
                meaning["review_mode"] = "confident"
                meaning["iteration"] = iteration
                meaning["loop_diagnostics"] = diagnostics
                return meaning

            if self._looping(iteration, progress):
                break

            previous_confidence = confidence
            working_input = self._refine_input(working_input, attempt=iteration)

        fallback_meaning = best_meaning or self.interpret(input_data, source=source)
        fallback_meaning = dict(fallback_meaning)
        fallback_meaning["review_mode"] = "best_guess"
        fallback_meaning["uncertainty"] = "high"
        fallback_meaning["confidence"] = round(float(fallback_meaning.get("confidence", 0.0)), 3)
        fallback_meaning["loop_diagnostics"] = diagnostics

        # Recovery pass: simplify once more and keep if confidence improves.
        simplified_input = self._refine_input(input_data, attempt=MAX_ITERATIONS)
        recovery = self.interpret(simplified_input, source=source)
        recovery_confidence = float(recovery.get("confidence", 0.0))
        if recovery_confidence > float(fallback_meaning.get("confidence", 0.0)):
            fallback_meaning = dict(recovery)
            fallback_meaning["review_mode"] = "recovered"
            fallback_meaning["uncertainty"] = "medium"
            fallback_meaning["loop_diagnostics"] = diagnostics + [
                {
                    "iteration": MAX_ITERATIONS + 1,
                    "input": str(simplified_input),
                    "confidence": round(recovery_confidence, 3),
                    "progress": "recovery",
                }
            ]

        return fallback_meaning

    def loop(self, input_data: Any, source: str = "unknown") -> Dict[str, Any]:
        meaning = self._iterative_interpret(input_data, source=source)
        self.state.current_input = input_data
        self.state.current_meaning = meaning
        self.connect(meaning, source_name="Player")
        self.update_memory(meaning, source=source)
        action = self.act(meaning)
        self.reflect()

        if meaning.get("review_mode") == "best_guess":
            self.state.marker = "UNCERTAIN"
        elif meaning.get("review_mode") == "recovered":
            self.state.marker = "RECOVERED"

        return {
            "meaning": meaning,
            "action": action,
            "state": self.state.snapshot(),
            "memory_size": self.memory.size(),
            "entity_summary": self.entities.summary(),
            "loop_policy": {
                "max_iterations": MAX_ITERATIONS,
                "confidence_threshold": CONFIDENCE_THRESHOLD,
                "min_progress": MIN_PROGRESS,
            },
        }


def create_engine() -> OroboroMind:
    return OroboroMind()
