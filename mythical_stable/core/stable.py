"""
mythical_stable.core.stable
============================
Stable — a composition-based container for Creature objects.
StableIterator — a custom iterator that yields in-stable creatures by power.

Stable *has* a list internally. It does not extend list. This gives full
control over the public interface: add() enforces uniqueness, remove() is
by name, and iteration order is defined by this class, not by list.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterator

if TYPE_CHECKING:
    from mythical_stable.core.creatures import Creature
    from mythical_stable.protocols import SortStrategy


class StableIterator:
    """Iterates over creatures that are currently in the stable, strongest first.

    Filtering and sorting happen at construction time — the snapshot is fixed
    when the iterator is created. Sending a creature on a mission mid-iteration
    does not affect the current traversal.

    Stable is an *iterable* (has __iter__ returning a new iterator each time).
    StableIterator is an *iterator* — has __iter__ returning self, and __next__
    advancing state. An iterable can be traversed many times; an iterator is
    single-use.
    """

    def __init__(self, creatures: list["Creature"]) -> None:
        available = [c for c in creatures if c._in_stable]
        self._snapshot: list["Creature"] = sorted(
            available, key=lambda c: c.power_level, reverse=True
        )
        self._index: int = 0

    def __iter__(self) -> "StableIterator":
        """Return self — iterators are their own iterables."""
        return self

    def __next__(self) -> "Creature":
        """Advance and return the next available creature."""
        if self._index >= len(self._snapshot):
            raise StopIteration
        creature = self._snapshot[self._index]
        self._index += 1
        return creature


class Stable:
    """A container for Creature objects.

    Composition over inheritance: Stable *has* a list of creatures — it does
    not *extend* list. This gives full control over the public interface:
    add() enforces uniqueness, remove() is by name, and the iteration order
    is defined by the class, not by list's internal ordering.

    Special methods make Stable feel native to Python:
        len(stable), "Frostbite" in stable, stable["Ember"], for c in stable
    """

    def __init__(self) -> None:
        self._creatures: list["Creature"] = []

    # ── mutation ──────────────────────────────────────────────────────────────

    def add(self, creature: "Creature") -> None:
        """Register a creature. Raises ValueError if a creature with the same name already exists."""
        if creature.name in self:
            raise ValueError(f"A creature named '{creature.name}' is already registered.")
        self._creatures.append(creature)

    def remove(self, name: str) -> None:
        """Remove a creature by name. Raises KeyError if not found."""
        creature = self[name]
        self._creatures.remove(creature)

    def find(self, name: str) -> "Creature":
        """Return the creature with the given name. Raises KeyError if not found."""
        for creature in self._creatures:
            if creature.name == name:
                return creature
        raise KeyError(f"No creature named '{name}' in the stable.")

    # ── container special methods ─────────────────────────────────────────────

    def __len__(self) -> int:
        return len(self._creatures)

    def __contains__(self, name: object) -> bool:
        """Support: 'Frostbite' in stable."""
        if not isinstance(name, str):
            return False
        return any(c.name == name for c in self._creatures)

    def __iter__(self) -> Iterator["Creature"]:
        """Support: for creature in stable."""
        return iter(self._creatures)

    def __getitem__(self, name: str) -> "Creature":
        """Support: stable['Ember']."""
        return self.find(name)

    def __repr__(self) -> str:
        names = [c.name for c in self._creatures]
        return f"Stable({len(self)} creatures: {names})"

    # ── iteration helpers ─────────────────────────────────────────────────────

    def available_by_power(self) -> StableIterator:
        """Return a StableIterator over in-stable creatures by power descending."""
        return StableIterator(self._creatures)

    def sorted(self, strategy: "SortStrategy") -> list["Creature"]:
        """Return creatures sorted according to the given SortStrategy."""
        return strategy.sort(list(self._creatures))