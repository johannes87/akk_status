from enum import Enum

class AKKState(Enum):
    CLOSED = 1
    OPEN_NO_SERVICE = 2
    OPEN_SELF_SERVICE = 3
    OPEN_FULL_SERVICE = 4


class State:
    def __init__(self):
        self._state_value = None

    def set_state_value(self, state_value):
        self._state_value = state_value
    
    def get_state_value(self):
        return self._state_value

