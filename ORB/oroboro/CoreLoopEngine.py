from __future__ import annotations

from .runtime import build_runtime


if __name__ == "__main__":
    runtime = build_runtime()
    runtime.run_pygame()
