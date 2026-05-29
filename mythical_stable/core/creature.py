from abc import abstractmethod, ABC
import random
from mythical_stable.core import utils as u


"""
==============================================================================
CLASS CREATURE (ABSTRACT)
==============================================================================
"""
class Creature(ABC):

    _total_creatures = 0
    __VALID_SPECIES = ["Dragon", "Phoenix", "Griffin", "Unicorn", "Basilisk"]

    """
    ==Constructor==
    """
    def __init__(self, name: str, species: str, origin: str, power_level: int | float, **kwargs) -> None:

        super().__init__(**kwargs)
        if origin == "":
            raise ValueError("You must provide a origin")

        #None
        self._name = None
        self._species = None
        self._power_level = None

        #Setters
        self.name = name
        self.species = species
        self.power_level = power_level

        #Privates
        self._origin = origin
        self._in_stable = True

        Creature._total_creatures += 1
    """
    Display Name, Specie, Origin and status of the creature when using print()
    """
    def __str__(self):
        status = u.green("In Stable") if self._in_stable else u.red("On Mission")
        return f"{u.blue(self._name)} - LvL {self._power_level} {u.yellow("<", self._species, ">")} (origin: {self._origin!r}) [{status}]"

    def __repr__(self):
        return f"Creature(name={self._name!r},species={self._species!r},origin={self._origin!r},power_level={self._power_level})"

    """
    ==Get - Set==
    """
    @property
    def name(self) -> str:
        return self._name
    @name.setter
    def name(self, name: str) -> None:
        if not isinstance(name, str):
            raise ValueError("Invalid name.\rName must be a string")
        else:
            if name == "":
                raise ValueError("You must provide a name")
            else:
                self._name = name

    @property
    def species(self) -> str:
        return self._species
    @species.setter
    def species(self, species: str) -> None:
        if not isinstance(species, str):
            raise ValueError("Invalid species.\rSpecies must be a string")
        else:
            status = type(self).is_valid_species(species)
            if not status:
                raise ValueError("Invalid species")
            else:
                self._species = species

    @property
    def origin(self) -> str:
        return self._origin

    @property
    def power_level(self) -> int | float:
        return self._power_level
    @power_level.setter
    def power_level(self, power_level: int | float) -> None:
        if not isinstance(power_level, (int, float)):
            raise ValueError("Invalid power level.\rPower level must be an int or a float.")
        else:
            status = type(self).is_valid_power_level(power_level)
            if not status:
                raise ValueError("Power level must be between 0 and 100")
            else:
                self._power_level = power_level

    """
    ==Methods==
    """
    def send_on_mission(self) -> None:
        """
        when sent on mission, the creature is out of the stable
        :return: False
        """
        self._in_stable = False

    def return_to_stable(self) -> None:
        """
        When returning to the stable, the creature is in the stable again
        :return: True
        """
        self._in_stable = True

    def send_to_field(self) -> None:
        """
        Describe the creature, its abilities. Warn that it's gone on mission and used the "send_on_mission" function
        :return: None
        """
        print(self)
        print(self.describe_abilities())
        print(f"{self.name} will be gone on mission "
              f"for {self.mission_duration_days()} days.")
        self.send_on_mission()

    def return_from_mission(self) -> None:
        """
        Warn that the creature is back from mission after "X" days and earned random exp then use the "return_to_stable" function
        :return: None
        """
        print(f"{self.name} came back from his mission "
              f"after {self.mission_duration_days()} days "
              f"and earned {random.randint(25,75)} Exp.")
        self.return_to_stable()

    def end_of_day_report(creatures: list):
        for creature in creatures:
            print(f"--- {creature.name} ---")
            print(creature.describe_abilities())
            print(
                f"Mission duration if sent: {creature.mission_duration_days()} days")
            print(creature)

    """
    ==Class Methods==
    """
    @classmethod
    def get_total_creatures(cls) -> None:
        """
        Prints the total number of creatures
        :return:
        """
        print("Total Creatures:", cls._total_creatures)

    @classmethod
    def add_from_dict(cls, data: dict):
        """
        Adds a creature from a dictionary
        :param data: data:dict
        :return: class:Creature
        """
        return cls(
            data["name"],
            data["species"],
            data["origin"],
            data["power_level"]
        )

    @classmethod
    def add_from_string(cls, creature_string: str):
        """
        Adds a creature from a string
        :param creature_string: string
        :return: class:Creature
        """

        name, species, origin, power_level = creature_string.split(",")
        return cls(
            name,
            species,
            origin,
            int(power_level)
        )

    """
     ==Static Methods==
    """

    @staticmethod
    def is_valid_species(species: str) -> bool:
        """
        Checks if the given species is valid for the creature
        :param species: string
        :return:
        """
        return species in Creature.__VALID_SPECIES

    @staticmethod
    def is_valid_power_level(level: int | float) -> bool:
        """
        Checks if the given power level is valid for the creature
        :param level: int or float
        :return: boolean
        """
        return level > 0 or level < 100

    """
    ==Abstract Methods==
    """

    @abstractmethod
    def mission_duration_days(self) -> int:
        ...

    @abstractmethod
    def describe_abilities(self) -> str:
        ...
