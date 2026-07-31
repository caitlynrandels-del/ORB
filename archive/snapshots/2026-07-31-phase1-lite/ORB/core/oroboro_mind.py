from __future__ import annotations

from typing import Any, Dict

from core.state import OroboroState
from core.memory import MemoryStore
from core.entity import Entity, EntitySystem
from language.interpreter import LanguageInterpreter


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

    def loop(self, input_data: Any, source: str = "unknown") -> Dict[str, Any]:
        self.perceive(input_data, source=source)
        meaning = self.interpret(input_data, source=source)
        self.connect(meaning, source_name="Player")
        self.update_memory(meaning, source=source)
        action = self.act(meaning)
        self.reflect()
        return {
            "meaning": meaning,
            "action": action,
            "state": self.state.snapshot(),
            "memory_size": self.memory.size(),
            "entity_summary": self.entities.summary(),
        }


def create_engine() -> OroboroMind:
    return OroboroMind()
