import datetime
from typing import Dict, Callable

from src.domain.payment.dto import PaymentGroupEnum


class GroupStrategySelector:
    __slots__ = ('_group_type', 'group_expression', 'sort_keys', 'convert_to_iso')

    _group_type: PaymentGroupEnum
    convert_to_iso: Callable[[Dict[str, int]], str]

    def __init__(self, group_type: PaymentGroupEnum):
        self._group_type = group_type

        self.group_expression: Dict[str, Dict[str, str]] = {}
        self.sort_keys: Dict[str, int] = {}

        if self._group_type == PaymentGroupEnum.HOUR:
            self._hour_expressions_strategy()
            self.convert_to_iso = self._hour_convert_to_iso_strategy

        elif self._group_type == PaymentGroupEnum.DAY:
            self._day_expressions_strategy()
            self.convert_to_iso = self._day_convert_to_iso_strategy

        elif self._group_type == PaymentGroupEnum.WEEK:
            self._week_expressions_strategy()
            self.convert_to_iso = self._week_convert_to_iso_strategy

        elif self._group_type == PaymentGroupEnum.MONTH:
            self._month_expressions_strategy()
            self.convert_to_iso = self._month_convert_to_iso_strategy

        else:
            raise ValueError("Invalid group type")

    def _hour_expressions_strategy(self):
        self.group_expression = {
            "year": {"$year": "$dt"},
            "month": {"$month": "$dt"},
            "day": {"$dayOfMonth": "$dt"},
            "hour": {"$hour": "$dt"}
        }
        self.sort_keys = {
            "_id.year": 1, "_id.month": 1, "_id.day": 1, "_id.hour": 1
        }

    def _day_expressions_strategy(self):
        self.group_expression = {
            "year": {"$year": "$dt"},
            "month": {"$month": "$dt"},
            "day": {"$dayOfMonth": "$dt"}
        }
        self.sort_keys = {
            "_id.year": 1, "_id.month": 1, "_id.day": 1
        }

    def _week_expressions_strategy(self):
        self.group_expression = {
            "year": {"$isoWeekYear": "$dt"},
            "week": {"$isoWeek": "$dt"}
        }
        self.sort_keys = {
            "_id.year": 1, "_id.week": 1
        }

    def _month_expressions_strategy(self):
        self.group_expression = {
            "year": {"$year": "$dt"},
            "month": {"$month": "$dt"}
        }
        self.sort_keys = {
            "_id.year": 1, "_id.month": 1
        }

    @staticmethod
    def _hour_convert_to_iso_strategy(group_id: Dict[str, int]) -> str:
        return datetime.datetime(group_id["year"], group_id["month"], group_id["day"], group_id["hour"]).isoformat()

    @staticmethod
    def _day_convert_to_iso_strategy(group_id: Dict[str, int]) -> str:
        return datetime.datetime(group_id["year"], group_id["month"], group_id["day"]).isoformat()

    @staticmethod
    def _week_convert_to_iso_strategy(group_id: Dict[str, int]) -> str:
        return datetime.datetime.strptime(f'{group_id["year"]} {group_id["week"]} 1', '%G %V %u').isoformat()

    @staticmethod
    def _month_convert_to_iso_strategy(group_id: Dict[str, int]) -> str:
        return datetime.datetime(group_id["year"], group_id["month"], 1).isoformat()
