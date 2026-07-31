from __future__ import annotations


class World:
    def __init__(self, name: str = "Oroboro World") -> None:
        self.name = name
        self.entities = []

    def add_entity(self, entity: object) -> None:
        self.entities.append(entity)
