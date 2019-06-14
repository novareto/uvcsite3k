from enum import IntEnum


STATES_NAMES = {
    0: 'Entwurf',
    1: 'gesendet',
    2: 'in Verarbeitung',
    3: 'Review'
}


class State(IntEnum):
    CREATED = 0
    PUBLISHED = 1
    PROGRESS = 2
    REVIEW = 3

    @property
    def title(self):
        return STATES_NAMES[self.value]
