from enum import Enum

class State(Enum):
    SUCCESS     = 0
    COMPENSATED = 1
    FAILURE     = 2
    CREATED     = 3
    RUNNING     = 4

class StatefulEntity:
    def __init__(self):
        self._state = state

    @property
    def state(self):
        return self._state

    @property
    def complete(self):
        return self._state in [State.COMPENSATED, State.SUCCESS, State.FAILURE]

    @property
    def success(self):
        return self._state in [State.COMPENSATED, State.SUCCESS]

    @property
    def failure(self):
        return self._state == State.FAILURE