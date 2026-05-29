# Group Exercise - Build the `mythical_stable` package

You will build **mythical_stable** - a real, pip-installable Python package.  
Once installed, anyone can use it with:

```bash
python -m pip install -e .
python -m mythical_stable        # run the demo
python -m pytest tests/ -v       # run all tests
```

The package is split into **three sub-packages**. Each person owns one and writes tests for someone else's.

| Person | Owns                        | Tests                        |
| ------ | --------------------------- | ---------------------------- |
| **A**  | `core/` + `pyproject.toml`  | `test_services.py` (tests B) |
| **B**  | `services/`                 | `test_patterns.py` (tests C) |
| **C**  | `patterns/` + `conftest.py` | `test_core.py` (tests A)     |

---

## Package structure

```
mythical_stable/
    __init__.py              ← re-exports the full public API
    protocols.py             ← shared contracts (agreed together on day 1)
    core/
        __init__.py
        creatures.py
        stable.py
        mission_record.py
    services/
        __init__.py
        mission_service.py
        dispatcher.py
        notifiers.py
    patterns/
        __init__.py
        strategies.py
        observers.py
        commands.py
tests/
    conftest.py              ← shared fixtures - owned by Person C
    test_core.py             ← written by Person C, tests Person A's code
    test_services.py         ← written by Person A, tests Person B's code
    test_patterns.py         ← written by Person B, tests Person C's code
pyproject.toml               ← packaging config - owned by Person A
README.md
```

---

## Step 0 - Write `protocols.py` together (20 min)

Before splitting, the three of you write `protocols.py` together.  
This file defines the structural contracts that cross sub-package boundaries.  
**No implementation here - contracts only.**

```python
from __future__ import annotations
from typing import Protocol

class MissionLogger(Protocol):
    def log_departure(self, record) -> None: ...
    def log_return(self, creature_name: str) -> None: ...

class MissionNotifier(Protocol):
    def notify(self, message: str) -> None: ...

class SortStrategy(Protocol):
    def sort(self, creatures: list) -> list: ...

class Command(Protocol):
    def execute(self) -> None: ...
    def undo(self) -> None: ...
```

Agree on the signatures, commit the file, then split.

---

## Person A - `core/` + packaging + `test_services.py`

### What you implement

**`core/creatures.py`**

- `Creature` abstract base class with all methods and properties
- `Dragon`, `Phoenix`, `Unicorn` subclasses
- `power_level` property with validation (0–100)
- One-line docstrings on every public class and method

**`core/mission_record.py`**

- `MissionRecord` dataclass with `__post_init__` validation
- `return_date` and `is_overdue` properties
- Manual `__eq__` and `__hash__` (same `creature_name` + `departure_date` = duplicate)
- `close()` method

**`core/stable.py`**

- `Stable` class (composition, not inheritance)
- `StableIterator` with `__iter__` / `__next__`
- Container special methods: `__len__`, `__contains__`, `__iter__`, `__getitem__`
- `available_by_power()` returning a `StableIterator`
- `sorted(strategy)` method

**`core/__init__.py`**

```python
from .creatures import Creature, Dragon, Phoenix, Unicorn
from .stable import Stable, StableIterator
from .mission_record import MissionRecord
```

**`pyproject.toml`** - you own this

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "mythical-stable"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = []

[project.optional-dependencies]
dev = ["pytest>=7"]

[project.scripts]
mythical-stable = "mythical_stable.__main__:main"
```

Once this is in place, everyone can run `pip install -e .` and imports will work.

### What you test - `test_services.py`

You test Person B's `services/` sub-package. Read the protocols and docstrings - do not look at the implementation.

**MissionService**

- `dispatch()` creates a `MissionRecord` and marks the creature as on mission
- `dispatch()` raises `RuntimeError` if the creature is already on a mission
- `recall()` marks the creature as returned and closes the record
- `recall()` raises `KeyError` if the creature has no active mission
- `active_missions()` returns the correct list of open records
- The logger is called on dispatch and on recall

**MissionDispatcher**

- `dispatch()` calls `notify()` on the injected notifier
- Works with any object that has a `notify(message)` method

**Tip : use a capturing logger in your tests, not `ConsoleMissionLogger`:**

```python
class CapturingLogger:
    def __init__(self): self.log = []
    def log_departure(self, record): self.log.append(("departed", record.creature_name))
    def log_return(self, name): self.log.append(("returned", name))
```

---

## Person B - `services/` + `test_patterns.py`

### What you implement

**`services/mission_service.py`**

- `MissionService(stable, logger)` - dependency injection
- `dispatch(creature_name, destination, duration_days, notes="")` → `MissionRecord`
  - Creates a `MissionRecord`, calls `send_on_mission()`, calls `logger.log_departure()`
  - Uses `mission_lock` context manager to prevent double-dispatch
  - Raises `RuntimeError` if creature is already on a mission
- `recall(creature_name)` - closes record, calls `return_to_stable()`, calls `logger.log_return()`
  - Raises `KeyError` if creature has no active mission
- `active_missions()` → `list[MissionRecord]`
- `ScrollArchive` class context manager and `mission_lock` generator context manager

**`services/dispatcher.py`**

- `MissionDispatcher(notifier)` - dependency injection
- `dispatch(creature_name, destination)` - calls `self._notifier.notify()` with a formatted message
- Does **not** send the creature on a mission - that is `MissionService`'s job

**`services/notifiers.py`**

- `ScrollNotifier` - prints to console with a scroll prefix
- `MirrorNotifier` - appends to `mirror_log.txt`
- `SilentNotifier` - no-op, does nothing
- `SilentLogger` - no-op logger for use in tests
- `ConsoleMissionLogger` - prints departure and return notices
- None of these inherit from the Protocol classes - structural typing only

**`services/__init__.py`**

```python
from .mission_service import MissionService, ScrollArchive, mission_lock
from .dispatcher import MissionDispatcher
from .notifiers import ConsoleMissionLogger, SilentLogger, ScrollNotifier, MirrorNotifier, SilentNotifier
```

> **If Person A hasn't finished yet:** create a minimal stub locally so you can run your own tests. Remove it once Person A's code is merged.

### What you test - `test_patterns.py`

You test Person C's `patterns/` sub-package.

**Strategy**

- `SortByName` returns creatures in alphabetical order
- `SortByPower` returns creatures highest power first
- `SortByAvailability` returns in-stable creatures before on-mission ones
- `stable.sorted(strategy)` returns a new list and does not modify the stable

**EventBus**

- A listener registered for an event is called when that event is published
- A listener for event X is not called when event Y is published
- Multiple listeners on the same event are all called
- Publishing an event with no listeners does not raise

**Command / CommandHistory**

- `DispatchCommand.execute()` dispatches the creature
- `DispatchCommand.undo()` recalls the creature
- `CommandHistory.undo_last()` reverses the most recent command
- `CommandHistory.undo_last()` on an empty history raises `IndexError`

---

## Person C - `patterns/` + `conftest.py` + `test_core.py`

### What you implement

**`patterns/strategies.py`**

- `SortByPower` - sort by `power_level` descending
- `SortByName` - sort alphabetically by `creature.name`
- `SortByAvailability` - in-stable first, then on-mission, then by name within each group

**`patterns/observers.py`**

- `EventBus` - `subscribe(event, fn)`, `publish(event, payload)`
- `audit_logger(payload)` - prints a timestamped audit line
- `overdue_checker(record)` - warns if a recalled record was overdue

**`patterns/commands.py`**

- `DispatchCommand` - `execute()` dispatches, `undo()` recalls
- `RecallCommand` - `execute()` recalls, `undo()` re-dispatches
- `CommandHistory` - `execute(cmd)`, `undo_last()`, `redo_last()`

**`patterns/__init__.py`**

```python
from .strategies import SortByPower, SortByName, SortByAvailability
from .observers import EventBus, audit_logger, overdue_checker
from .commands import DispatchCommand, RecallCommand, CommandHistory
```

**`conftest.py`** - you own this, it provides fixtures to all three test files

```python
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
```

### What you test - `test_core.py`

You test Person A's `core/` sub-package.

**Creature subclasses**

- `Dragon.mission_duration_days()` returns 14
- `Phoenix.mission_duration_days()` returns 7
- `Unicorn.mission_duration_days()` returns 3
- `Unicorn.send_on_mission()` raises `RuntimeError` when `power_level < 50`
- `Unicorn.send_on_mission()` succeeds when `power_level >= 50`
- `Phoenix.resurrect()` increments `resurrection_count`
- `power_level` setter raises `ValueError` for out-of-range values

**MissionRecord**

- `return_date` = `departure_date` + `timedelta(days=duration_days)`
- Two records with same `creature_name` + `departure_date` are equal and have the same hash
- `__post_init__` raises `ValueError` for empty `destination`
- `__post_init__` raises `ValueError` for non-positive `duration_days`
- `is_overdue` is `True` only when active and `return_date` is in the past
- `is_overdue` is `False` after `close()`

**Stable**

- `add()` raises `ValueError` when a creature with the same name is added twice
- `remove()` raises `KeyError` for an unknown name
- `__contains__` returns `True` for a registered creature's name
- `__len__` returns the correct count after add and remove
- `__iter__` iterates over all creatures
- `available_by_power()` only returns in-stable creatures, in descending power order

---

## Running the tests

```bash
# All tests
python -m pytest tests/ -v

# One file at a time
python -m pytest tests/test_core.py -v
python -m pytest tests/test_services.py -v
python -m pytest tests/test_patterns.py -v

# Stop at first failure
python -m pytest tests/ -x
```

All tests must pass before the exercise is considered complete.  
**If your tests find a bug in someone else's code - report it, don't fix it. The author fixes their own code.**

---

## Deliverables checklist

- [ ] `pip install -e .` works from a clean environment
- [ ] `python -m mythical_stable` runs the demo without errors
- [ ] `python -m pytest tests/` runs with **zero failures**
- [ ] Every public class and method has a one-line docstring
- [ ] `README.md` contains install instructions and a usage example

## Bonus - if you finish early

- Add type annotations on every method and run `mypy mythical_stable/` with zero errors
- Write `tests/test_integration.py` - a full scenario: register three creatures, dispatch two, recall one, sort by power, undo a command
- Add a `__version__ = "0.1.0"` in `mythical_stable/__init__.py`
