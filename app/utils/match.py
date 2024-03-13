from enum import Enum


class MatchStatus(Enum):
    NS = 1
    IN_PROGRESS = 2
    FINISHED = 3
    ABANDONED = 4

    @classmethod
    def all_statuses(cls) -> list:
        return [value.name for name, value in vars(cls).items() if name.isupper()]
