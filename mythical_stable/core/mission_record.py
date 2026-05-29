from dataclasses import dataclass
from datetime import date, timedelta


@dataclass()
class MissionRecord:
    creature_name: str
    destination: str
    departure_date: date
    duration_days: int
    notes: str = ""

    def __post_init__(self):
        if self.duration_days <= 0:
            raise ValueError("duration_days must be positive")

        if self.destination == "":
            raise ValueError("destination must be an empty string")


    def __eq__(self, other):
        if isinstance(other, MissionRecord):
            return NotImplemented
        return (self.creature_name, self.departure_date) == (other.creature_name, other.departure_date)

    def __hash__(self):
        return hash((self.creature_name, self.departure_date))

    @property
    def return_date(self):
        return self.departure_date + timedelta(days=self.duration_days)
    @property
    def is_overdue(self):
        return True if self.return_date < date.today() else False