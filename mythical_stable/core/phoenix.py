from core.creature import Creature
from core.fly_mixin import FlyMixin


"""
==============================================================================
CLASS PHOENIX (CREATURE)
==============================================================================
"""

class Phoenix(FlyMixin, Creature):

    _total_phoenixes : int = 0

    def __init__(self, name , species, origin, power_level):
        super().__init__(name=name,species= species, origin=origin, power_level=power_level)

        self.__resurrection_count = 0

        type(self)._total_phoenixes += 1

    def __str__(self):
        base = super().__str__()
        return f"{base}"

    @property
    def resurrection_count(self) -> int:
        return self.__resurrection_count

    @classmethod
    def get_total_creatures(cls) -> None:
        """
        Print the total number of Phoenixes
        :return:
        """
        print("Total Phoenixes:", cls._total_phoenixes)

    def mission_duration_days(self) -> int:
        """
        Duration of the mission counted in days
        :return: int (7)
        """
        return 7

    def describe_abilities(self) -> str:
        """
        Describe the abilities of the Phoenix
        :return: string with creature.name & creature.element
        """
        return (f"{self.name} has a flame aura and has the ability to fly. "
                f"{self.name} can also resurrect upon death.")

    def death(self) -> None:
        """
        Prints the message that the creature died and starts the resurrect function
        :return: None
        """
        print(f"{self.name} failed the mission and died bursting to flames.")
        self.resurrect()

    def resurrect(self) -> None:
        """
        Counts the total number of deaths and prints the message
        :return:
        """
        self.__resurrection_count += 1
        print(f"{self.name} resurrects from its ashes.")