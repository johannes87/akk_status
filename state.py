from enum import Enum

class AKKState(Enum):
    CLOSED = 1
    OPEN_NO_SERVICE = 2
    OPEN_SELF_SERVICE = 3
    OPEN_FULL_SERVICE = 4


class CurrentAKKState:
    def __init__(self):
        self._state = None

    def set_state(self, state):
        self._state = state
    
    def get_state(self):
        return self._state

