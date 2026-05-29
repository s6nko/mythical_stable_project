"""
7 — Observer
BEHAVIORAL

What is it?
The Observer pattern (also called Publish/Subscribe or Event Bus) lets multiple independent listeners react to events
without being coupled to the publisher. The publisher emits named events; each listener subscribes to the events it
cares about and is called automatically.

Why does it matter?
Without Observer, a service that needs to notify multiple things on dispatch — log it, check for overdue missions,
trigger an alert — must call each one explicitly, and importing each notifier couples MissionService to all of them.
Observer removes that coupling: the service just publishes an event, and listeners self-register.

Where to implement it in the Stable
MissionService already uses an injected logger. But logging is just one reaction to a dispatch event. An EventBus lets
any number of independent listeners — an AuditLogger, an OverdueChecker, a RoyalNotifier — subscribe to
'mission_dispatched' and 'mission_recalled' without MissionService knowing they exist.

EventBus: subscribe(event_name, listener_fn), publish(event_name, payload).
'mission_dispatched' event carries the MissionRecord as payload.
'mission_recalled' event carries the creature_name string as payload.
AuditLogger listener: prints a timestamped audit line on every event.
OverdueChecker listener: on 'mission_recalled', checks if the record was overdue and prints a warning.
Your tasks
Implement EventBus with subscribe(event, fn) and publish(event, payload). Store subscribers in a dict[str, list[callable]].
Wire EventBus into MissionService: inject it via __init__, call self._bus.publish() at the end of dispatch() and recall().
Write an AuditLogger function (not a class — a plain function is a valid listener) that prints a timestamped entry.
Write an OverdueChecker function that checks the record's is_overdue on 'mission_recalled'.
Subscribe both listeners and confirm they are both called on every dispatch and recall, in subscription order.

"""
from datetime import datetime
from typing import Callable

from mythical_stable import MissionRecord


class EventBus:
    def __init__(self):
        self._listeners: dict[str, list[Callable]] = {}

    def subscribe(self, event: str, fn: Callable) -> None:
        """
        Register fn to be called whenever event is published.
        """
        self._listeners.setdefault(event, []).append(fn)

    def publish(self, event: str, payload) -> None:
        """Call every subscriber registered for event with payload."""
        for fn in self._listeners.get(event, []):
            fn(payload)

# ── Built-in listener functions ───────────────────────────────────────────────

def audit_logger(payload) -> None:
    """Print a timestamped audit line for any event payload."""
    print(f"[AUDIT {datetime.now():%H:%M:%S}] {payload}")


def overdue_checker(record: "MissionRecord") -> None:
    """Warn if the recalled mission record was overdue."""
    if record.is_overdue:
        print(f"⚠️  OVERDUE: {record.creature_name} was due back on {record.return_date}")