from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Entity:
    name: str
    data: Dict[str, Any] = field(default_factory=dict)
    connections: List[Dict[str, Any]] = field(default_factory=list)
    resolved: bool = False
    confidence: float = 0.0
    last_signal: Optional[str] = None

    def connect(self, entity: "Entity", meaning: Dict[str, Any], strength: float = 1.0) -> Dict[str, Any]:
        record = {
            "target": entity.name,
            "meaning": meaning,
            "strength": strength,
        }
        self.connections.append(record)
        entity.last_signal = meaning.get("concept")
        return record


class EntitySystem:
    def __init__(self) -> None:
        self.entities: List[Entity] = []

    def add_entity(self, entity: Entity) -> Entity:
        self.entities.append(entity)
        return entity

    def get_entity(self, name: str) -> Optional[Entity]:
        for entity in self.entities:
            if entity.name.lower() == name.lower():
                return entity
        return None

    def connect_entities(self, source_name: str, target_name: str, meaning: Dict[str, Any], strength: float = 1.0) -> Optional[Dict[str, Any]]:
        source = self.get_entity(source_name)
        target = self.get_entity(target_name)
        if not source or not target:
            return None
        return source.connect(target, meaning, strength=strength)

    def mark_resolved(self, name: str, resolved: bool = True) -> None:
        entity = self.get_entity(name)
        if entity is not None:
            entity.resolved = resolved

    def summary(self) -> Dict[str, Any]:
        return {
            "count": len(self.entities),
            "resolved": sum(1 for entity in self.entities if entity.resolved),
            "entities": [entity.name for entity in self.entities],
        }
