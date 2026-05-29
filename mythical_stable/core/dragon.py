from core.creature import Creature
from core import utils as u
from core.fly_mixin import FlyMixin

"""
==============================================================================
CLASS DRAGON (CREATURE)
==============================================================================
"""


class Dragon(FlyMixin, Creature):

    _total_dragons = 0

    def __init__(self, name , species, origin, power_level, element: str):
        super().__init__(name=name,species= species, origin=origin, power_level=power_level)

        self._element = None
        self.element = element

        type(self)._total_dragons += 1

    def __str__(self):
        status = u.green("In Stable") if self._in_stable else u.red("On Mission")
        return f"{u.blue(self._name)} - LvL {self._power_level} {u.yellow("<[",self.element,"]", self._species, ">")} (origin: {self._origin!r}) [{status}]"

    @property
    def element(self):
        return self._element
    @element.setter
    def element(self,element):
        if not isinstance(element, str):
            raise TypeError("Element must be a string")
        else:
            self._element = element

    def mission_duration_days(self) -> int:
        """
        Duration of the mission counted in days
        :return: int (14)
        """
        return 14

    def describe_abilities(self) -> str:
        """
        Describe the abilities of the dragon
        :return: string with creature.name & creature.element
        """
        return f"{self.name} breathes {self.element.lower()} and flies at great speed."

    @classmethod
    def get_total_creatures(cls) -> None:
        """
        Prints the total of dragons
        :return: None
        """
        print("Total Dragons:", cls._total_dragons)

