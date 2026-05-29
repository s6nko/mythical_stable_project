'''
8 — Command
BEHAVIORAL

What is it?
The Command pattern encapsulates a request as an object. Each command object knows how to execute an action and,
crucially, how to undo it. A CommandHistory stack stores executed commands and enables undo/redo by replaying or
reversing them in order.

Why does it matter?
Once an action is an object, it becomes composable, storable, and reversible. A stable master who accidentally
dispatches the wrong creature can undo the last command rather than manually recreating the previous state.
This is the foundation of every undo/redo system, transaction log, and macro recorder.

Where to implement it in the Stable
Dispatching and recalling creatures are natural commands. DispatchCommand executes a dispatch and can undo it
with a recall. RecallCommand executes a recall and can undo it with a re-dispatch. CommandHistory.undo_last() pops
and reverses the last executed command.

Command Protocol: execute() -> None and undo() -> None.
DispatchCommand(service, name, destination, days): execute() calls service.dispatch(), undo() calls service.recall().
RecallCommand(service, name): execute() calls service.recall(), undo() re-dispatches (store record data at construction
time).
CommandHistory: a stack (list) of executed commands. execute(cmd) runs and pushes; undo_last() pops and undoes.
Your tasks
Define a Command Protocol with execute() and undo().
Implement DispatchCommand and RecallCommand.
Implement CommandHistory with execute(cmd) and undo_last(). undo_last() must raise IndexError (or print a warning) if
the history is empty.
Demonstrate: dispatch Frostbite, dispatch Ember, undo last (Ember returns), undo last (Frostbite returns). Print stable
state after each step.
Bonus: add redo_last() — this requires a separate redo stack.

'''
from typing import Protocol


class Command(Protocol):
    def execute(self) -> None:
        ...

    def undo(self) -> None:
        ...

class DispatchCommand(Command):
    def __init__(self, service, name, destination, days):
        self._service = service
        self._name = name
        self._destination = destination
        self._days = days
        self._executed = False

    def execute(self) -> None:
        self._service.dispatch(self._name, self._destination, self._days)
        self._executed = True

    def undo(self) -> None:
        if self._executed:
            self._service.recall(self._name)


class RecallCommand(Command):
    def __init__(self, service, name):
        self._service = service
        self._name = name
        self._executed = False

    def execute(self) -> None:
        self._service.recall(self._name)
        self._executed = True

    def undo(self) -> None:
        if self._executed:
            self._service.dispatch(self._name)


class CommandHistory:
    def __init__(self):
        self._command_stack : list[Command]= []
        self._top = -1

    def execute(self, cmd:Command):
        cmd.execute()
        self._top += 1
        if self._top >= len(self._command_stack):
            self._command_stack.append(cmd)
        else:
            self._command_stack[self._top] = cmd
        self._command_stack = self._command_stack[0:self._top+1] # Remove elements invalidated by the new cmd

    def undo_last(self):
        if not self._command_stack or self._top < 0:
            raise IndexError
        else:
            self._command_stack[self._top].undo()
            self._top -= 1

    def redo_last(self):
        if self._top >= len(self._command_stack):
            raise IndexError
        else:
            self._top += 1
            self._command_stack[self._top].execute()