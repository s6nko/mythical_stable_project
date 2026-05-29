"""
mythical_stable.services.mission_service
=========================================
MissionService — orchestrates creature dispatching and recall.
ScrollArchive  — file-backed context manager for mission logs.
mission_lock   — @contextmanager that prevents double-dispatch.

MissionService uses dependency injection: both the logger and the stable are
passed in. Swap SilentLogger for ConsoleMissionLogger with no code changes
to the service itself.
"""

from __future__ import annotations

from contextlib import contextmanager
from datetime import date
from typing import TYPE_CHECKING, Iterator

from core.creature import Creature
from core.mission_record import MissionRecord
from core.stable import Stable
from protocols import MissionLogger

if TYPE_CHECKING:
    pass


# ── Context managers ──────────────────────────────────────────────────────────

class ScrollArchive:
    """File-backed mission archive managed as a context manager.

    __enter__ opens the file and returns self so the 'as' clause works.
    __exit__ always closes the file — returning False ensures exceptions
    propagate normally rather than being suppressed.
    """

    def __init__(self, filepath: str) -> None:
        self._filepath = filepath
        self._file = None

    def __enter__(self) -> "ScrollArchive":
        """Open the archive file and return self."""
        self._file = open(self._filepath, "a", encoding="utf-8")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """Close the archive file; propagate any exception."""
        if self._file:
            self._file.close()
            self._file = None
        return False   # do not suppress exceptions

    def _require_open(self) -> None:
        """Raise RuntimeError if the archive is not open."""
        if self._file is None or self._file.closed:
            raise RuntimeError(
                "Scroll is not open. Use 'with ScrollArchive(...) as scroll:'."
            )

    def write_departure(self, record: MissionRecord) -> None:
        """Append a departure entry. Must be called inside a 'with' block."""
        self._require_open()
        self._file.write(
            f"DEPARTED | {record.creature_name} → {record.destination} "
            f"| {record.departure_date} → {record.return_date}\n"
        )

    def write_return(self, creature_name: str) -> None:
        """Append a return entry. Must be called inside a 'with' block."""
        self._require_open()
        self._file.write(f"RETURNED | {creature_name}\n")


@contextmanager
def mission_lock(creature: Creature) -> Iterator[Creature]:
    """Prevent a creature from being double-dispatched via a boolean lock flag.

    Uses @contextmanager instead of a full class because the logic is simple:
    set a flag, yield, clear it. A finally block guarantees the lock is
    released even if an exception is raised inside the 'with' block.
    """
    if getattr(creature, "_locked", False):
        raise RuntimeError(f"{creature.name} is already being processed.")
    creature._locked = True
    try:
        yield creature
    finally:
        creature._locked = False


# ── MissionService ────────────────────────────────────────────────────────────

class MissionService:
    """Orchestrates creature dispatching and recall.

    Dependency injection: the logger is passed in — MissionService never
    creates it internally. Swap ConsoleMissionLogger for SilentLogger in
    tests and the service behaves identically with no console output.
    """

    def __init__(self, stable: Stable, logger: MissionLogger) -> None:
        self._stable = stable
        self._logger = logger
        self._active: dict[str, MissionRecord] = {}

    def dispatch(
        self,
        creature_name: str,
        destination: str,
        duration_days: int,
        notes: str = "",
    ) -> MissionRecord:
        """Send a creature on a mission and create a MissionRecord for it."""
        if creature_name in self._active:
            raise RuntimeError(f"{creature_name} is already on an active mission.")

        creature = self._stable[creature_name]

        with mission_lock(creature):
            record = MissionRecord(
                creature_name=creature_name,
                destination=destination,
                departure_date=date.today(),
                duration_days=duration_days,
                notes=notes,
            )
            creature.send_on_mission()
            self._active[creature_name] = record
            self._logger.log_departure(record)

        return record

    def recall(self, creature_name: str) -> None:
        """Return a creature from its mission and close the record."""
        if creature_name not in self._active:
            raise KeyError(f"{creature_name} has no active mission.")

        creature = self._stable[creature_name]
        record = self._active.pop(creature_name)
        record.close()
        creature.return_to_stable()
        self._logger.log_return(creature_name)

    def active_missions(self) -> list[MissionRecord]:
        """Return all currently open mission records."""
        return list(self._active.values())