import unittest
from mythical_stable.core import Stable, Dragon
from mythical_stable.services import MissionService, MissionDispatcher



class CapturingLogger:
    def __init__(self): self.log = []
    def log_departure(self, record): self.log.append(("departed", record.creature_name))
    def log_return(self, name): self.log.append(("returned", name))

class TestServices(unittest.TestCase):

    def setUp(self):
        self.stable = Stable()
        self.dragon = Dragon("Frostbite", "Dragon", "Nordic Realms", 95, element="ice")
        self.stable.add(self.dragon)
        self.logger = CapturingLogger()
        self.service = MissionService(self.stable, self.logger)


    def tearDown(self):
        self.stable = None
        self.dragon = None
        self.logger = None
        self.service = None
        self.mock_service = None

    """
    Mission Service Tests
    """

    def test_dispatch_creates_mission_record(self):
        self.service.dispatch("Frostbite", "FrozenPeaks", 5)

    def test_dispatch_raises_runtime_error(self):
        self.service.dispatch("Frostbite", "FrozenPeaks", 5)
        with self.assertRaises(RuntimeError):
            self.service.dispatch("Frostbite", "FrozenPeaks", 5)

    def test_recall_a_creature(self):
        self.service.dispatch("Frostbite", "FrozenPeaks", 5)
        self.service.recall("Frostbite")

    def test_recall_raises_a_key_error(self):
        pass
    def test_active_mission_list_open_records(self):
        pass

    """
    Mission Dispatcher Tests
    """
    def test_dispatch_calls_notify(self):
        pass
    def test_notify_method(self):
        pass

