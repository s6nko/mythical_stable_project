import pytest
from mythical_stable.core import Dragon, Phoenix, Unicorn, Stable

@pytest.fixture
def frostbite():
    return Dragon("Frostbite", "Nordic Realms", 95, element="ice")

@pytest.fixture
def ember():
    return Phoenix("Ember", "Ashlands", 80)

@pytest.fixture
def stardust():
    return Unicorn("Stardust", "Silver Meadows", 72)

@pytest.fixture
def tinsel():
    return Unicorn("Tinsel", "Soft Glades", 30)

@pytest.fixture
def populated_stable(frostbite, ember, stardust):
    s = Stable()
    s.add(frostbite)
    s.add(ember)
    s.add(stardust)
    return s