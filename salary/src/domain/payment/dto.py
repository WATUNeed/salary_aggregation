import datetime
from enum import Enum
from typing import List

from beanie import PydanticObjectId

from src.domain.abc.dto import AbstractDTO


class PaymentCreateDTO(AbstractDTO):
    value: int
    dt: datetime.datetime


class PaymentUpdateDTO(AbstractDTO):
    _id: PydanticObjectId
    value: int
    dt: datetime.datetime


class SumPeriodGroupEnum(Enum):
    HOUR = 'hour'
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'


class SumByPeriodInputDTO(AbstractDTO):
    dt_from: datetime.datetime
    dt_upto: datetime.datetime
    group_type: SumPeriodGroupEnum


class SumByPeriodOutputDTO(AbstractDTO):
    dataset: List[int]
    labels: List[str]
