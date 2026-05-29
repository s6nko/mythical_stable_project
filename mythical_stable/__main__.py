"""
mythical_stable.__main__
=========================
CLI entry point. Run with:  python -m mythical_stable
Or, after pip install:      mythical-stable
"""

from __future__ import annotations


def main() -> None:
    """Run a quick demo of the installed package."""
    from mythical_stable import (
        Stable, Dragon, Phoenix, Unicorn,
        MissionService, SilentLogger,
        SortByPower, SortByName, SortByAvailability,
        EventBus, audit_logger,
        DispatchCommand, CommandHistory,
    )

    print("=" * 56)
    print("  mythical_stable — installed package demo")
    print("=" * 56)

    # ── Setup ──────────────────────────────────────────────────────────────────
    stable = Stable()
    stable.add(Dragon("Frostbite", "Nordic Realms", 95, element="ice"))
    stable.add(Phoenix("Ember", "Ashlands", 80))
    stable.add(Unicorn("Stardust", "Silver Meadows", 72))
    stable.add(Unicorn("Tinsel", "Soft Glades", 30))

    print(f"\nStable: {stable!r}")

    # ── MissionService ─────────────────────────────────────────────────────────
    print("\n── MissionService ──────────────────────────────")
    svc = MissionService(stable, SilentLogger())
    svc.dispatch("Frostbite", "Frozen Peaks", 14)
    svc.dispatch("Ember", "Volcanic Rift", 7)
    print(f"Active missions: {[r.creature_name for r in svc.active_missions()]}")
    svc.recall("Frostbite")
    print(f"After recall:    {[r.creature_name for r in svc.active_missions()]}")

    # ── Strategy ───────────────────────────────────────────────────────────────
    print("\n── Strategy (sorting) ──────────────────────────")
    for strategy in (SortByName(), SortByPower(), SortByAvailability()):
        names = [c.name for c in stable.sorted(strategy)]
        print(f"  {type(strategy).__name__:<22} → {names}")

    # ── EventBus ───────────────────────────────────────────────────────────────
    print("\n── EventBus (Observer) ─────────────────────────")
    bus = EventBus()
    bus.subscribe("mission_dispatched", audit_logger)
    svc2 = MissionService(stable, SilentLogger())

    # Manually publish an event to demonstrate the bus
    from mythical_stable.core import MissionRecord
    from datetime import date
    rec = MissionRecord("Stardust", "Silver Forest", date.today(), 3)
    bus.publish("mission_dispatched", rec)

    # ── Command / Undo ─────────────────────────────────────────────────────────
    print("\n── Command + Undo ──────────────────────────────")
    svc3 = MissionService(stable, SilentLogger())
    history = CommandHistory()
    history.execute(DispatchCommand(svc3, "Stardust", "Silver Forest", 3))
    print(f"After dispatch:  Stardust in stable = {stable['Stardust']._in_stable}")
    history.undo_last()
    print(f"After undo:      Stardust in stable = {stable['Stardust']._in_stable}")

    print("\n✅ All good — package is working correctly.")
    print("   Run 'pytest tests/' to execute the full test suite.\n")


if __name__ == "__main__":
    main()