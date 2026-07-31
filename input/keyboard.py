from __future__ import annotations

from typing import Dict, List


class KeyboardInput:
    def __init__(self) -> None:
        self.keys: List[str] = []

    def update(self, pressed: List[str]) -> None:
        self.keys = pressed
