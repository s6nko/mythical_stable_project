"""
mythical_stable
===============
A pip-installable OOP training package built around a mythical creature stable.

Quick start::

    from mythical_stable import Stable, Dragon, Phoenix, Unicorn
    from mythical_stable import MissionService, SilentLogger
    from mythical_stable import SortByPower, EventBus

    stable = Stable()
    stable.add(Dragon("Frostbite", "Nordic Realms", 95, element="ice"))
    stable.add(Phoenix("Ember", "Ashlands", 80))

    svc = MissionService(stable, SilentLogger())
    svc.dispatch("Frostbite", "Frozen Peaks", 14)
    print(svc.active_missions())
"""

__version__ = "0.1.0"

# ── core ──────────────────────────────────────────────────────────────────────
from mythical_stable.core import (
    Creature,
    Dragon,
    Phoenix,
    Unicorn,
    Stable,
    StableIterator,
    MissionRecord,
)

# ── protocols ─────────────────────────────────────────────────────────────────
from mythical_stable.protocols import (
    MissionLogger,
    MissionNotifier,
    SortStrategy,
    Command,
)

# ── services ──────────────────────────────────────────────────────────────────
from mythical_stable.services import (
    MissionService,
    MissionDispatcher,
    ScrollArchive,
    mission_lock,
    ScrollNotifier,
    MirrorNotifier,
    SilentNotifier,
    SilentLogger,
    ConsoleMissionLogger,
)

# ── patterns ──────────────────────────────────────────────────────────────────
from mythical_stable.patterns import (
    SortByPower,
    SortByName,
    SortByAvailability,
    EventBus,
    audit_logger,
    overdue_checker,
    DispatchCommand,
    RecallCommand,
    CommandHistory,
)

__all__ = [
    # core
    "Creature", "Dragon", "Phoenix", "Unicorn",
    "Stable", "StableIterator", "MissionRecord",
    # protocols
    "MissionLogger", "MissionNotifier", "SortStrategy", "Command",
    # services
    "MissionService", "MissionDispatcher",
    "ScrollArchive", "mission_lock",
    "ScrollNotifier", "MirrorNotifier", "SilentNotifier",
    "SilentLogger", "ConsoleMissionLogger",
    # patterns
    "SortByPower", "SortByName", "SortByAvailability",
    "EventBus", "audit_logger", "overdue_checker",
    "DispatchCommand", "RecallCommand", "CommandHistory",
]