import datetime

from src.domain.abc.dto import AbstractDTO


class PeriodDTO(AbstractDTO):
    from_dt: datetime.datetime
    to_dt: datetime.datetime
