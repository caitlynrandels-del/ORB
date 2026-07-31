from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List


@dataclass
class MemoryRecord:
    source: str
    meaning: Dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class MemoryStore:
    def __init__(self) -> None:
        self.records: List[MemoryRecord] = []

    def remember(self, meaning: Dict[str, Any], source: str = "unknown") -> MemoryRecord:
        record = MemoryRecord(source=source, meaning=meaning)
        self.records.append(record)
        return record

    def latest(self) -> MemoryRecord | None:
        return self.records[-1] if self.records else None

    def size(self) -> int:
        return len(self.records)

    def snapshot(self) -> List[Dict[str, Any]]:
        return [
            {
                "source": record.source,
                "meaning": record.meaning,
                "timestamp": record.timestamp,
            }
            for record in self.records
        ]
