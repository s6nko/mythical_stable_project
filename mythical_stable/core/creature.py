"""
mythical_stable.core.creatures
===============================
Abstract base class Creature and the three concrete subclasses:
Dragon, Phoenix, and Unicorn.

Every creature has a name, species, origin, and power_level. The power_level
is validated on assignment (0–100). Two abstract methods — mission_duration_days()
and describe_abilities() — must be implemented by every subclass.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterator


class Creature(ABC):
    """Abstract base for all stable creatures. Enforces the mission interface."""

    _total_creatures: int = 0

    def __init__(self, name: str, species: str, origin: str, power_level: float) -> None:
        self.name = name
        self.species = species
        self.__origin = origin
        self._power_level: float | None = None
        self.power_level = power_level          # goes through the validated setter
        self._in_stable: bool = True
        Creature._total_creatures += 1

    # ── abstract interface ────────────────────────────────────────────────────

    @abstractmethod
    def mission_duration_days(self) -> int:
        """Return the number of days this creature is typically away on a mission."""

    @abstractmethod
    def describe_abilities(self) -> str:
        """Return a human-readable description of this creature's abilities."""

    # ── state transitions ─────────────────────────────────────────────────────

    def send_on_mission(self) -> None:
        """Mark the creature as deployed on a mission."""
        self._in_stable = False

    def return_to_stable(self) -> None:
        """Mark the creature as returned to the stable."""
        self._in_stable = True

    # ── power_level property with validation ──────────────────────────────────

    @property
    def power_level(self) -> float:
        """Current power level (0–100)."""
        return self._power_level

    @power_level.setter
    def power_level(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise ValueError(f"power_level must be a number, got {type(value).__name__}.")
        if not (0 <= value <= 100):
            raise ValueError(f"power_level must be between 0 and 100, got {value}.")
        self._power_level = float(value)

    @property
    def origin(self) -> str:
        """Read-only origin of the creature (name-mangled for encapsulation)."""
        return self.__origin

    # ── class-level helpers ───────────────────────────────────────────────────

    @classmethod
    def get_total_creatures(cls) -> int:
        """Return the total number of Creature instances created across all subclasses."""
        return cls._total_creatures

    @staticmethod
    def is_valid_species(species: str) -> bool:
        """Return True if species is on the recognised stable species list."""
        return species in ["Dragon", "Ice Dragon", "Phoenix", "Griffin", "Unicorn", "Basilisk"]

    # ── dunder methods ────────────────────────────────────────────────────────

    def __str__(self) -> str:
        status = "in stable" if self._in_stable else "on mission"
        return f"{self.name} the {self.species} (origin: {self.origin}) [{status}]"

    def __repr__(self) -> str:
        return (
            f"Creature(name={self.name!r}, species={self.species!r}, "
            f"origin={self.origin!r}, power_level={self.power_level!r})"
        )


# ── Concrete subclasses ───────────────────────────────────────────────────────

class Dragon(Creature):
    """A fire- (or element-) breathing dragon."""

    def __init__(self, name: str, origin: str, power_level: float, element: str = "fire") -> None:
        super().__init__(name=name, species="Dragon", origin=origin, power_level=power_level)
        self.element = element

    def mission_duration_days(self) -> int:
        """Dragons take 14 days per mission."""
        return 14

    def describe_abilities(self) -> str:
        """Return a description of this dragon's combat abilities."""
        return (
            f"{self.name} breathes {self.element} and flies at great speed, "
            f"capable of destroying fortifications in a single pass."
        )

    def __str__(self) -> str:
        status = "in stable" if self._in_stable else "on mission"
        return f"{self.name} the Dragon [{self.element}] (origin: {self.origin}) [{status}]"

    def __repr__(self) -> str:
        return (
            f"Dragon(name={self.name!r}, origin={self.origin!r}, "
            f"power_level={self.power_level!r}, element={self.element!r})"
        )


class Phoenix(Creature):
    """A flame-wreathed phoenix that can resurrect."""

    def __init__(self, name: str, origin: str, power_level: float) -> None:
        super().__init__(name=name, species="Phoenix", origin=origin, power_level=power_level)
        self.resurrection_count: int = 0

    def mission_duration_days(self) -> int:
        """Phoenixes take 7 days per mission."""
        return 7

    def describe_abilities(self) -> str:
        """Return a description of this phoenix's abilities."""
        return (
            f"{self.name} is wreathed in an aura of living flame and resurrects "
            f"upon death (resurrections so far: {self.resurrection_count})."
        )

    def resurrect(self) -> None:
        """Increment the resurrection counter and announce the rebirth."""
        self.resurrection_count += 1
        print(f"🔥 {self.name} rises from the ashes! Resurrection #{self.resurrection_count}.")

    def __repr__(self) -> str:
        return (
            f"Phoenix(name={self.name!r}, origin={self.origin!r}, "
            f"power_level={self.power_level!r}, resurrection_count={self.resurrection_count!r})"
        )


class Unicorn(Creature):
    """A healing unicorn that refuses to deploy below power level 50."""

    def __init__(self, name: str, origin: str, power_level: float) -> None:
        super().__init__(name=name, species="Unicorn", origin=origin, power_level=power_level)

    def mission_duration_days(self) -> int:
        """Unicorns take 3 days per mission."""
        return 3

    def describe_abilities(self) -> str:
        """Return a description of this unicorn's abilities."""
        return (
            f"{self.name} can heal wounds, neutralise poison, and outrun "
            f"any mount — but must not be sent out alone if weakened."
        )

    def send_on_mission(self) -> None:
        """Refuse deployment if power level is below 50."""
        if self.power_level < 50:
            raise RuntimeError(
                f"{self.name} has power level {self.power_level} — too low for a solo mission."
            )
        super().send_on_mission()

    def __repr__(self) -> str:
        return (
            f"Unicorn(name={self.name!r}, origin={self.origin!r}, "
            f"power_level={self.power_level!r})"
        )