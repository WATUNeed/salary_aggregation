import datetime
from typing import Self

from src.domain.abc.dto import AbstractDTO


class PeriodDTO(AbstractDTO):
    from_dt: datetime.datetime
    to_dt: datetime.datetime

    @classmethod
    def validate_from_input(cls, from_dt: datetime.datetime, to_dt: datetime.datetime) -> Self:
        if from_dt > to_dt:
            raise ValueError
        return cls(
            from_dt=from_dt,
            to_dt=to_dt
        )
