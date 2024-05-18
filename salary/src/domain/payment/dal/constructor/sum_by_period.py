import abc
import datetime
from typing import Dict

from src.domain.payment.dto import SumPeriodGroupEnum
from src.domain.period.dto import PeriodDTO


class SumByPeriodStrategyABC(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def match_fabric(period: PeriodDTO) -> Dict[str, Dict[str, datetime.datetime]]:
        ...

    @staticmethod
    @abc.abstractmethod
    def group_fabric() -> Dict[str, Dict[str, str]]:
        ...

    @staticmethod
    @abc.abstractmethod
    def sort_fabric() -> Dict[str, int]:
        ...

    @staticmethod
    @abc.abstractmethod
    def round_to_period_edge(period: PeriodDTO) -> PeriodDTO:
        ...

    @staticmethod
    @abc.abstractmethod
    def convert_to_iso(group_id: Dict[str, int]) -> str:
        ...

    @staticmethod
    @abc.abstractmethod
    def increment(dt: datetime) -> datetime.datetime:
        ...


class HourSumByPeriodStrategy(SumByPeriodStrategyABC):

    @staticmethod
    def match_fabric(period: PeriodDTO) -> Dict[str, Dict[str, datetime.datetime]]:
        return {
            "dt": {
                "$gte": period.from_dt,
                "$lt": period.to_dt
            }
        }

    @staticmethod
    def group_fabric() -> Dict[str, Dict[str, str]]:
        return {
            "_id": {
                "year": {"$year": "$dt"},
                "month": {"$month": "$dt"},
                "day": {"$dayOfMonth": "$dt"},
                "hour": {"$hour": "$dt"}
            },
            "total": {
                "$sum": "$value"
            }
        }

    @staticmethod
    def sort_fabric() -> Dict[str, int]:
        return {
            "_id.year": 1, "_id.month": 1, "_id.day": 1, "_id.hour": 1
        }

    @staticmethod
    def round_to_period_edge(period: PeriodDTO) -> PeriodDTO:
        if period.to_dt.minute != 0 or period.to_dt.second != 0:
            period.to_dt = period.to_dt.replace(minute=59, second=59)
        return period

    @staticmethod
    def convert_to_iso(group_id: Dict[str, int]) -> str:
        return datetime.datetime(group_id["year"], group_id["month"], group_id["day"], group_id["hour"]).isoformat()

    @staticmethod
    def increment(dt: datetime) -> datetime.datetime:
        return dt + datetime.timedelta(hours=1)


class DaySumByPeriodStrategy(SumByPeriodStrategyABC):

    @staticmethod
    def match_fabric(period: PeriodDTO) -> Dict[str, Dict[str, datetime.datetime]]:
        return {
            "dt": {
                "$gte": period.from_dt,
                "$lt": period.to_dt
            }
        }

    @staticmethod
    def group_fabric() -> Dict[str, Dict[str, str]]:
        return {
            "_id": {
                "year": {"$year": "$dt"},
                "month": {"$month": "$dt"},
                "day": {"$dayOfMonth": "$dt"}
            },
            "total": {
                "$sum": "$value"
            }
        }

    @staticmethod
    def sort_fabric() -> Dict[str, int]:
        return {
            "_id.year": 1, "_id.month": 1, "_id.day": 1
        }

    @staticmethod
    def round_to_period_edge(period: PeriodDTO) -> PeriodDTO:
        if period.to_dt.hour != 0 or period.to_dt.minute != 0 or period.to_dt.second != 0:
            period.to_dt = period.to_dt.replace(hour=23, minute=59, second=59)
        return period

    @staticmethod
    def convert_to_iso(group_id: Dict[str, int]) -> str:
        return datetime.datetime(group_id["year"], group_id["month"], group_id["day"]).isoformat()

    @staticmethod
    def increment(dt: datetime) -> datetime.datetime:
        return dt + datetime.timedelta(days=1)


class WeekSumByPeriodStrategy(SumByPeriodStrategyABC):

    @staticmethod
    def match_fabric(period: PeriodDTO) -> Dict[str, Dict[str, datetime.datetime]]:
        return {
            "dt": {
                "$gte": period.from_dt,
                "$lt": period.to_dt
            }
        }

    @staticmethod
    def group_fabric() -> Dict[str, Dict[str, str]]:
        return {
            "_id": {
                "year": {"$isoWeekYear": "$dt"},
                "week": {"$isoWeek": "$dt"}
            },
            "total": {
                "$sum": "$value"
            }
        }

    @staticmethod
    def sort_fabric() -> Dict[str, int]:
        return {
            "_id.year": 1, "_id.week": 1
        }

    @staticmethod
    def round_to_period_edge(period: PeriodDTO) -> PeriodDTO:
        to_weekday = period.to_dt.isoweekday()
        if to_weekday != 7 or period.to_dt.hour != 0 or period.to_dt.minute != 0 or period.to_dt.second != 0:
            week_start = period.to_dt + datetime.timedelta(days=(7 - to_weekday))
            period.to_dt = week_start.replace(hour=23, minute=59, second=59)
        return period

    @staticmethod
    def convert_to_iso(group_id: Dict[str, int]) -> str:
        return datetime.datetime.strptime(f'{group_id["year"]} {group_id["week"]} 1', '%G %V %u').isoformat()

    @staticmethod
    def increment(dt: datetime) -> datetime.datetime:
        return dt + datetime.timedelta(weeks=1)


class MonthSumByPeriodStrategy(SumByPeriodStrategyABC):

    @staticmethod
    def match_fabric(period: PeriodDTO) -> Dict[str, Dict[str, datetime.datetime]]:
        return {
            "dt": {
                "$gte": period.from_dt,
                "$lt": period.to_dt
            }
        }

    @staticmethod
    def group_fabric() -> Dict[str, Dict[str, str]]:
        return {
            "_id": {
                "year": {"$year": "$dt"},
                "month": {"$month": "$dt"}
            },
            "total": {
                "$sum": "$value"
            }
        }

    @staticmethod
    def sort_fabric() -> Dict[str, int]:
        return {
            "_id.year": 1, "_id.month": 1
        }

    @staticmethod
    def round_to_period_edge(period: PeriodDTO) -> PeriodDTO:
        if period.to_dt.day != 1 or period.to_dt.hour != 0 or period.to_dt.minute != 0 or period.to_dt.second != 0:
            next_month = period.to_dt.replace(day=28) + datetime.timedelta(days=4)
            last_day_of_month = (next_month - datetime.timedelta(days=next_month.day))
            period.to_dt = last_day_of_month.replace(hour=23, minute=59, second=59)
        return period

    @staticmethod
    def convert_to_iso(group_id: Dict[str, int]) -> str:
        return datetime.datetime(group_id["year"], group_id["month"], 1).isoformat()

    @staticmethod
    def increment(dt: datetime) -> datetime.datetime:
        month = dt.month + 1
        year = dt.year
        if month > 12:
            month = 1
            year += 1
        return datetime.datetime(year, month, 1)


class SumByPeriodGroupingSelector:
    __slots__ = (
        'period', 'group_type', '_strategy', 'period', 'match', 'group', 'sort', 'convert_to_iso', 'increment'
    )

    def __init__(self, period: PeriodDTO, group_type: SumPeriodGroupEnum):
        self.period = period
        self.group_type = group_type

        if group_type == SumPeriodGroupEnum.HOUR:
            self._strategy = HourSumByPeriodStrategy

        elif group_type == SumPeriodGroupEnum.DAY:
            self._strategy = DaySumByPeriodStrategy

        elif group_type == SumPeriodGroupEnum.WEEK:
            self._strategy = WeekSumByPeriodStrategy

        elif group_type == SumPeriodGroupEnum.MONTH:
            self._strategy = MonthSumByPeriodStrategy

        else:
            raise ValueError('Invalid group_type')

        self.period = self._strategy.round_to_period_edge(self.period)
        self.match = self._strategy.match_fabric(self.period)
        self.group = self._strategy.group_fabric()
        self.sort = self._strategy.sort_fabric()

        self.convert_to_iso = self._strategy.convert_to_iso
        self.increment = self._strategy.increment
