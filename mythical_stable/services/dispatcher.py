"""
mythical_stable.services.dispatcher
=====================================
MissionDispatcher — sends notifications when a creature is dispatched.

The dispatcher receives a MissionNotifier via dependency injection and has no
knowledge of how the notification is delivered (console, file, email, etc.).
This is the Protocol exercise (ex. 10): the dispatcher works with any object
that has a notify(message: str) -> None method, regardless of its class hierarchy.
"""

from __future__ import annotations

from protocols import MissionNotifier


class MissionDispatcher:
    """Sends a notification whenever a mission event occurs.

    The notifier is injected at construction time. MissionDispatcher never
    creates or imports a concrete notifier — it depends only on the Protocol.
    """

    def __init__(self, notifier: MissionNotifier) -> None:
        self._notifier = notifier

    def dispatch(self, creature_name: str, destination: str) -> None:
        """Notify that a creature has been dispatched to a destination."""
        message = f"🐉 {creature_name} dispatched to {destination}."
        self._notifier.notify(message)

    def recall(self, creature_name: str) -> None:
        """Notify that a creature has been recalled from its mission."""
        message = f"🏠 {creature_name} has returned to the stable."
        self._notifier.notify(message)