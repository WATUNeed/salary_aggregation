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
    hour = 'hour'
    day = 'day'
    week = 'week'
    month = 'month'


class PaymentSumForPeriodDTO(AbstractDTO):
    dt_from: datetime.datetime
    dt_upto: datetime.datetime
    group_type: PaymentGroupEnum
