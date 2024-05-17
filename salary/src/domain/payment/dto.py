import datetime
from enum import Enum

from beanie import PydanticObjectId

from src.domain.abc.dto import AbstractDTO


class PaymentCreateDTO(AbstractDTO):
    value: int
    dt: datetime.datetime


class PaymentUpdateDTO(AbstractDTO):
    _id: PydanticObjectId
    value: int
    dt: datetime.datetime


class PaymentGroupEnum(Enum):
    HOUR = 'hour'
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'
