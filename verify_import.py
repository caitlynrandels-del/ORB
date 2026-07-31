from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def verify_core_engine() -> None:
    from core.oroboro_mind import create_engine

    engine = create_engine()
    result = engine.loop("verify import smoke test", source="verify_import")
    print("core import ok")
    print(f"core state: {result['state']['marker']}")


def verify_package_core_loop() -> None:
    from ORB.oroboro.core_loop import create_engine

    engine = create_engine()
    result = engine.loop("verify package loop", source="verify_import")
    print("package core_loop import ok")
    print(f"package state: {result['state']['marker']}")


def verify_optional_runtime() -> None:
	try:
		from ORB.oroboro.runtime import build_runtime
	except ModuleNotFoundError as exc:
		if exc.name == "pygame":
			print("runtime import skipped: pygame is not installed")
			return
		raise

	runtime = build_runtime()
	print("runtime import ok")
	print(f"runtime type: {type(runtime).__name__}")


def main() -> None:
	verify_core_engine()
	verify_package_core_loop()
	verify_optional_runtime()


if __name__ == "__main__":
	main()
