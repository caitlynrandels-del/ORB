from __future__ import annotations

from .core_loop import create_engine
from .midi_bridge import MidiInputBridge
from .pygame_bridge import PygameExplorationWorld


class OroboroRuntime:
    def __init__(self) -> None:
        self.engine = create_engine()
        self.midi = MidiInputBridge()

    def feed_midi(self, message: dict) -> dict:
        payload = self.midi.handle_message(message)
        return self.engine.loop(payload, source="midi")

    def run_pygame(self) -> None:
        world = PygameExplorationWorld()
        world.run()


def build_runtime() -> OroboroRuntime:
    return OroboroRuntime()
