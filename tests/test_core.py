'''
test_core.py

You test Person A's core/ sub-package.
'''

from datetime import timedelta, datetime, date
from unittest.mock import Mock, MagicMock

import pytest

from tests.conftest import frostbite, ember, stardust
from mythical_stable import Unicorn, MissionService, MissionLogger, MissionRecord, Stable, Creature

'''
Creature subclasses

    Dragon.mission_duration_days() returns 14
    Phoenix.mission_duration_days() returns 7
    Unicorn.mission_duration_days() returns 3
    Unicorn.send_on_mission() raises RuntimeError when power_level < 50
    Unicorn.send_on_mission() succeeds when power_level >= 50
    Phoenix.resurrect() increments resurrection_count
    power_level setter raises ValueError for out-of-range values

'''
def test_mission_duration_days(frostbite, ember, stardust):
    assert frostbite.mission_duration_days() == 14
    assert ember.mission_duration_days() == 7
    assert stardust.mission_duration_days() == 3

def test_send_on_mission(stardust):
    Unicorn("test1","test_origin", 50).send_on_mission()
    with pytest.raises(RuntimeError):
        Unicorn("test2", "test_origin", 49).send_on_mission()

def test_resurrect(ember):
    x = ember.resurrection_count
    ember.resurrect()
    assert ember.resurrection_count == x+1

def test_power_level(frostbite, ember, stardust):
    for creature in [frostbite, ember, stardust]:
        for power_level in [-1,101]:
            with pytest.raises(ValueError):
                creature.power_level = power_level
        for power_level in [0,100]:
            creature.power_level = power_level
            assert creature.power_level == power_level

'''
MissionRecord

    return_date = departure_date + timedelta(days=duration_days)
    Two records with same creature_name + departure_date are equal and have the same hash
    __post_init__ raises ValueError for empty destination
    __post_init__ raises ValueError for non-positive duration_days
    is_overdue is True only when active and return_date is in the past
    is_overdue is False after close()
'''

def test_return_date(populated_stable, frostbite, ember):
    mission_logger = MagicMock(MissionLogger)
    service = MissionService(populated_stable, mission_logger)
    for creature,duration in [(frostbite, 10), (ember,1)]:
        mission_record = service.dispatch(creature.name,"test destination",duration)
        assert mission_record.return_date == mission_record.departure_date + timedelta(days=duration)

def test_mission_record_hash(frostbite, ember):
    for creature in [frostbite]:
        mr1 = MissionRecord(creature.name,"somewhere", date.today(),10)
        mr2 = MissionRecord(creature.name,"elsewhere", date.today(),1)
        assert mr1.__hash__() == mr2.__hash__()
        mr1 = MissionRecord(creature.name,"somewhere", date.today(),10)
        mr2 = MissionRecord(creature.name,"elsewhere", date.today() + timedelta(days=1),1)
        assert mr1.__hash__() != mr2.__hash__()

def test_post_init(frostbite, ember):
    with pytest.raises(ValueError):
        mr1 = MissionRecord(frostbite.name,"", date.today(),10)
        mr2 = MissionRecord(frostbite.name,"", date.today(),-1)

def test_overdue(frostbite):
    for today_delta, duration, result in [(-11,10,True), (-1,1,False)]:
        mr1 = MissionRecord(frostbite.name, "somewhere", date.today() + timedelta(days=today_delta), duration)
        assert mr1.is_overdue is result
        mr1.close()
        assert mr1.is_overdue is False

'''
Stable

    add() raises ValueError when a creature with the same name is added twice
    remove() raises KeyError for an unknown name
    __contains__ returns True for a registered creature's name
    __len__ returns the correct count after add and remove
    __iter__ iterates over all creatures
    available_by_power() only returns in-stable creatures, in descending power order
'''

def test_add_remove(frostbite, ember, stardust):
    s = Stable()
    assert len(s) == 0

    s.add(frostbite)
    assert (frostbite.name in s) is True
    assert len(s) == 1

    with pytest.raises(ValueError):
        s.add(frostbite)
    assert len(s) == 1

    with pytest.raises(KeyError):
        s.remove("Donald Duck")
    assert len(s) == 1

    for creature in s:
        assert (creature.name in s) is True

    s.add(ember)
    s.add(stardust)
    for creature in s:
        assert (creature.name in s) is True

    assert [creature.power_level for creature in s.available_by_power()] == sorted([creature.power_level for creature in s], reverse=True)
    mission_logger = MagicMock(MissionLogger)
    service = MissionService(s, mission_logger)
    service.dispatch(frostbite.name, "test destination", 10)
    assert len(list(s.available_by_power())) == 2
    assert [creature.power_level for creature in s.available_by_power()] == sorted([creature.power_level for creature in [ember, stardust]], reverse=True)
