from enum import IntEnum


class State(IntEnum):
    CREATED = 0
    PUBLISHED = 1
    PROGRESS = 2
    REVIEW = 3
