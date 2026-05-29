"""
mythical_stable.core.mission_record
====================================
MissionRecord dataclass — a single mission log entry.

Two records are considered duplicates when they share the same creature_name
and departure_date (a creature cannot be double-booked on the same day).
__eq__ and __hash__ are defined manually (not via frozen=True) to demonstrate
that defining __eq__ silently sets __hash__ to None unless it is also defined.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class MissionRecord:
    """Immutable record of a single creature mission."""

    creature_name: str
    destination: str
    departure_date: date
    duration_days: int
    notes: str = field(default="")
    _active: bool = field(default=True, init=False, repr=False)

    def __post_init__(self) -> None:
        if not self.destination.strip():
            raise ValueError("destination must not be empty.")
        if not isinstance(self.duration_days, int) or self.duration_days <= 0:
            raise ValueError(
                f"duration_days must be a positive integer, got {self.duration_days!r}."
            )

    # ── computed properties ───────────────────────────────────────────────────

    @property
    def return_date(self) -> date:
        """Expected return date based on departure and duration."""
        return self.departure_date + timedelta(days=self.duration_days)

    @property
    def is_overdue(self) -> bool:
        """True if the expected return date has passed and the mission is still active."""
        return self._active and self.return_date < date.today()

    def close(self) -> None:
        """Mark this record as closed (creature has returned)."""
        self._active = False

    # ── equality by identity ──────────────────────────────────────────────────

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MissionRecord):
            return NotImplemented
        return (
            self.creature_name == other.creature_name
            and self.departure_date == other.departure_date
        )

    def __hash__(self) -> int:
        return hash((self.creature_name, self.departure_date))

    def __str__(self) -> str:
        status = "ACTIVE" if self._active else "CLOSED"
        overdue = " ⚠️  OVERDUE" if self.is_overdue else ""
        return (
            f"[{status}{overdue}] {self.creature_name} → {self.destination} "
            f"({self.departure_date} to {self.return_date})"
        )