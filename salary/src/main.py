import asyncio
import datetime

from src.database.mongo.model import init_models
from src.domain.payment.dal import PaymentDAO
from src.domain.payment.dto import PaymentGroupEnum
from src.domain.period.dto import PeriodDTO


async def main():
    await init_models()
    period = PeriodDTO(
        from_dt=datetime.datetime.fromisoformat("2022-10-01T00:00:00"),
        to_dt=datetime.datetime.fromisoformat("2022-11-30T23:59:00")
    )
    group_type = PaymentGroupEnum.DAY
    r = await PaymentDAO().get_sum_for_period_by_group_type(period, group_type)
    print(r)


if __name__ == '__main__':
    asyncio.run(main())
