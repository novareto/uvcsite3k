from enum import Enum


class States(Enum):
    NOT_INSTALLED = 'not installed'
    INSTALLED = 'installed'
    INCONSISTANT = 'inconsistant'


class ResultTypes(Enum):
    JSON = 'application/json'
    PLAIN = 'text/plain'
    MESSAGE = 'message/status'
