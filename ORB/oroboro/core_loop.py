from __future__ import annotations

from typing import Any, Dict, Optional

from .entity_system import Entity, EntitySystem
from .language_model import LanguageModel
from .memory import MemoryStore
from .sensors import SensorBridge


class OroboroCoreEngine:
    def __init__(self) -> None:
        self.entity_system = EntitySystem()
        self.memory = MemoryStore()
        self.language = LanguageModel()
        self.sensors = SensorBridge()
        self.state = {
            "marker": "AWAKENING",
            "current_input": None,
            "current_meaning": None,
            "last_action": None,
        }

        self._bootstrap_entities()

    def _bootstrap_entities(self) -> None:
        self.entity_system.add_entity(Entity("Player"))
        self.entity_system.add_entity(Entity("World"))
        self.entity_system.add_entity(Entity("Artifact", data={"type": "unknown object"}))
        self.entity_system.add_entity(Entity("Midi"))

    def perceive(self, input_data: Any, source: str = "unknown") -> Dict[str, Any]:
        self.state["current_input"] = input_data
        self.sensors.register(source, input_data)
        return {"source": source, "value": input_data}

    def interpret(self, input_data: Any, source: str = "unknown") -> Dict[str, Any]:
        context = {"source": source}
        meaning = self.language.interpret(input_data, context=context)
        self.state["current_meaning"] = meaning
        return meaning

    def connect_meaning(self, meaning: Dict[str, Any], source_name: str = "Player") -> None:
        for entity_name in meaning.get("entities", []):
            entity = self.entity_system.get_entity(entity_name)
            if entity is None:
                entity = self.entity_system.add_entity(Entity(entity_name))
            self.entity_system.connect_entities(source_name, entity.name, meaning)

        if self.entity_system.get_entity(source_name) is None:
            self.entity_system.add_entity(Entity(source_name))

    def update_memory(self, meaning: Dict[str, Any], source: str = "unknown") -> None:
        self.memory.remember(meaning, source=source)

    def act(self, meaning: Dict[str, Any]) -> Dict[str, Any]:
        intent = meaning.get("intent", "observe")
        action = {
            "intent": intent,
            "action_hint": meaning.get("action_hint", "observe"),
            "priority": meaning.get("priority", "normal"),
        }
        self.state["last_action"] = action
        return action

    def reflect(self) -> None:
        if self.state["current_meaning"] is None:
            self.state["marker"] = "AWAKENING"
            return

        if all(entity.resolved for entity in self.entity_system.entities):
            self.state["marker"] = "ALL_KNOWN"
        else:
            self.state["marker"] = "PROCESSING"

    def loop(self, input_data: Any, source: str = "unknown") -> Dict[str, Any]:
        self.perceive(input_data, source=source)
        meaning = self.interpret(input_data, source=source)
        self.connect_meaning(meaning, source_name="Player")
        self.update_memory(meaning, source=source)
        action = self.act(meaning)
        self.reflect()
        return {
            "meaning": meaning,
            "action": action,
            "state": self.state,
            "memory_size": self.memory.size(),
            "entity_summary": self.entity_system.summary(),
        }

    def bind_sensor(self, name: str, source: Any) -> None:
        self.sensors.register(name, source)


def create_engine() -> OroboroCoreEngine:
    return OroboroCoreEngine()
