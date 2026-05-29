from typing import TYPE_CHECKING, Iterator

if TYPE_CHECKING:
    from core.creature import Creature
    from protocols import SortStrategy

from core import utils as u



class Stable:
    def __init__(self):
        self._creatures: list[Creature] = []
        #self._robots: list[RoboticGuard] = []

    #Returns the number of creatures in the stable
    def __len__(self):
        return len(self._creatures)

    #Returns "True" if a creature with that name is present in the stable
    def __contains__(self, name: str):
        for creature in self._creatures:
            if creature.name == name:
                return True
        return False

    #Iterates over all creatures
    def __iter__(self) -> Iterator[Creature]:
        return iter(self._creatures)

    #stable[creature.name] -> same as find()
    def __getitem__(self,name: str):
        return self.find(name)

    #Stable('{len(Stable)} creatures: ["creature1", "creature2","creature3",...]
    def __repr__(self):
        names = [creature.name for creature in self._creatures]
        return f"Stable:({len(self)} creatures: {names})"

    #add(creature: Creature) (add a creature; raise ValueError if a creature with the same name already exists)
    def add(self, creature: Creature):
        """Register a creature. Raises ValueError if a creature with the same name already exists."""
        if creature.name in self:
            raise ValueError(
                f"The creature named {creature.name!r} is already in the stable.")
        else:
            self._creatures.append(creature)
            print(f"{u.blue(creature.name)}", u.green("has been added"),"to the stable.")

    #remove(name: str) (remove by name; raise KeyError if not found)
    def remove(self, name: str):
        """Remove a creature by name. Raises KeyError if not found."""
        creature = self.find(name)
        if creature.name not in self:
            raise KeyError(f"{creature.name!r} was not found in the stable.")
        else:
            self._creatures.remove(creature)
            print(f"{u.blue(creature.name)}", u.red("has been removed"),"to the stable.")

    #find(name: str) -> Creature (return the creature with that name; raise KeyError if not found)
    def find(self, name: str):
        """Return the creature with the given name. Raises KeyError if not found."""
        for creature in self:
            if creature.name == name:
                return creature

        raise KeyError(f"No creature named {name!r} was found.")

    def available_by_power(self) -> StableIterator:
        """Return a StableIterator over in-stable creatures by power descending."""
        return StableIterator(self._creatures)

    def sorted(self, strategy: "SortStrategy") -> list["Creature"]:
        """Return creatures sorted according to the given SortStrategy."""
        return strategy.sort(list(self._creatures))



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
