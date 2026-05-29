"""
mythical_stable.services.notifiers
====================================
Concrete MissionNotifier implementations and MissionLogger implementations.

None of these classes inherit from MissionNotifier or MissionLogger — they
satisfy the Protocols purely structurally (duck typing). A type-checker such
as mypy verifies compliance statically.
"""

from __future__ import annotations

from core.mission_record import MissionRecord


# ── MissionLogger implementations ─────────────────────────────────────────────

class ConsoleMissionLogger:
    """Logs mission events to stdout."""

    def log_departure(self, record: MissionRecord) -> None:
        """Print a departure notice to the console."""
        print(
            f"⚔️  DEPARTED  | {record.creature_name} → {record.destination} "
            f"| back by {record.return_date}"
        )

    def log_return(self, creature_name: str) -> None:
        """Print a return notice to the console."""
        print(f"🏠 RETURNED  | {creature_name} is back in the stable.")


class SilentLogger:
    """No-op logger — zero side effects. Ideal for tests."""

    def log_departure(self, record: MissionRecord) -> None:
        """Do nothing on departure."""

    def log_return(self, creature_name: str) -> None:
        """Do nothing on return."""


# ── MissionNotifier implementations ───────────────────────────────────────────

class ScrollNotifier:
    """Prints notifications to the console with a scroll prefix."""

    def notify(self, message: str) -> None:
        """Print the message to stdout with a scroll emoji prefix."""
        print(f"📜 [SCROLL] {message}")


class MirrorNotifier:
    """Appends notifications to mirror_log.txt."""

    def notify(self, message: str) -> None:
        """Append the message to mirror_log.txt."""
        with open("mirror_log.txt", "a", encoding="utf-8") as f:
            f.write(f"🪞 [MIRROR] {message}\n")


class SilentNotifier:
    """No-op notifier — does nothing. Satisfies MissionNotifier structurally."""

    def notify(self, message: str) -> None:
        """Deliver nothing."""