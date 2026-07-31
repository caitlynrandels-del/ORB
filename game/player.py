from __future__ import annotations


class Player:
    def __init__(self, name: str = "Player") -> None:
        self.name = name
        self.x = 0
        self.y = 0

    def move(self, dx: int = 0, dy: int = 0) -> None:
        self.x += dx
        self.y += dy
