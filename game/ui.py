from __future__ import annotations


class UIOverlay:
    def __init__(self) -> None:
        self.messages: list[str] = []

    def add_message(self, message: str) -> None:
        self.messages.append(message)
