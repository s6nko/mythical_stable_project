import pytest

from tests.conftest import frostbite, ember, stardust
from mythical_stable import Unicorn
'''
test_core.py

You test Person A's core/ sub-package.

Creature subclasses

    Dragon.mission_duration_days() returns 14
    Phoenix.mission_duration_days() returns 7
    Unicorn.mission_duration_days() returns 3
    Unicorn.send_on_mission() raises RuntimeError when power_level < 50
    Unicorn.send_on_mission() succeeds when power_level >= 50
    Phoenix.resurrect() increments resurrection_count
    power_level setter raises ValueError for out-of-range values

MissionRecord

    return_date = departure_date + timedelta(days=duration_days)
    Two records with same creature_name + departure_date are equal and have the same hash
    __post_init__ raises ValueError for empty destination
    __post_init__ raises ValueError for non-positive duration_days
    is_overdue is True only when active and return_date is in the past
    is_overdue is False after close()

Stable

    add() raises ValueError when a creature with the same name is added twice
    remove() raises KeyError for an unknown name
    __contains__ returns True for a registered creature's name
    __len__ returns the correct count after add and remove
    __iter__ iterates over all creatures
    available_by_power() only returns in-stable creatures, in descending power order
'''


def test_mission_duration_days(frostbite, ember, stardust):
    assert frostbite.mission_duration_days() == 14
    assert ember.mission_duration_days() == 7
    assert stardust.mission_duration_days() == 3

def test_send_on_mission(stardust):
    Unicorn("test1","test_origin", 50).send_on_mission()
    with pytest.raises(RuntimeError):
        Unicorn("test2", "test_origin", 49).send_on_mission()