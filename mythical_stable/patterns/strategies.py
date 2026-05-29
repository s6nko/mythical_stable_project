import protocols
'''
6 — Strategy
BEHAVIORAL

What is it?
The Strategy pattern defines a family of interchangeable algorithms and lets callers swap them at runtime without
changing the context that uses them. The context holds a reference to a strategy object and delegates the varying behaviour to it.

Why does it matter?
When a method needs to behave differently depending on a choice — sort by name, sort by power, sort by availability —
a chain of if/elif blocks is the naive solution. It grows with every new option and cannot be extended without modifying
 the method. Strategy turns each option into an object, and makes extension trivial: add a class, nothing else changes.

Where to implement it in the Stable
The Stable's iteration order is currently fixed. A stable master might want to view creatures sorted by power, by name,
or by availability. A SortStrategy plugged into Stable.sorted() makes sorting interchangeable at runtime.

SortStrategy Protocol: a single method sort(creatures: list[Creature]) -> list[Creature].
SortByPower: descending power_level — already the StableIterator default.
SortByName: alphabetical by creature.name.
SortByAvailability: in-stable creatures first, then those on missions.
Stable.available_by_power() becomes Stable.sorted(strategy: SortStrategy).
Your tasks
Define a SortStrategy Protocol with a sort(creatures) method.
Implement SortByPower, SortByName, and SortByAvailability.
Add a sorted(strategy: SortStrategy) method to Stable that returns a sorted list.
Demonstrate runtime swapping: call stable.sorted(SortByName()) then stable.sorted(SortByPower()) and print both results.
Bonus: add SortByMissionReturn that sorts on-mission creatures by their expected return_date (requires access to the MissionRepository).
'''

class SortStrategy(Protocol):
    def sort(self, creatures: list[Creature]) -> list[Creature]:
        ...

class SortByPower(SortStrategy):
    def sort(self, creatures: list[Creature]) -> list[Creature]:
        """
        sorting by descending power_level — already the StableIterator default.
        :param creatures:
        :return: the sorted Creature list
        """
        return sorted(creatures, key=lambda x: x.power_level, reverse=True)

class SortByName(SortStrategy):
    def sort(self, creatures: list[Creature]) -> list[Creature]:
        """
        alphabetical sorting by creature.name.
        :param creatures:
        :return: the sorted Creature list
        """
        return sorted(creatures, key=lambda x: x.name)

class SortByAvailability(SortStrategy):
    def sort(self, creatures: list[Creature]) -> list[Creature]:
        """
        stable sort in-stable creatures first, then those on missions.
        :param creatures:
        :return: the sorted Creature list
        """
        return [c for c in creatures if c.in_stable()] + [c for c in creatures if not c.in_stable()]

class SortByMissionReturn(SortStrategy):
    def sort(self, creatures: list[Creature], ) -> list[Creature]:
        """
        sorts on-mission creatures by their expected return_date (requires access to the MissionRepository).
        :param creatures:
        :return: the sorted Creature list
        """
        # return sorted([c for c in creatures if not c.in_stable()], key: lambda c: c.mission_record.return_date)
        raise NotImplementedError # Requires access to the in-mission creature's return_date

