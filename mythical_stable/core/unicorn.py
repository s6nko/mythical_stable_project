from core.creature import Creature

"""
==============================================================================
CLASS UNICORN (CREATURE)
==============================================================================
"""

class Unicorn(Creature):
    def __init__(self, name , species, origin, power_level):
        super().__init__(name, species, origin, power_level)

    def __str__(self):
        base = super().__str__()
        return f"{base}"

    def send_on_mission(self) -> None:
        if self._power_level < 50:
            raise RuntimeError(f"{self.name} can't be send in battle because it's too weak.")
        else:
            super().send_on_mission()

    def mission_duration_days(self) -> int:
        return 3

    def describe_abilities(self) -> str:
        return f"{self.name} can run fast and has healing abilities."