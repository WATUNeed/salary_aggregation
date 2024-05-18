from aiogram.utils.formatting import Text
from pydantic import ValidationError

from src.domain.payment.dal.dao import PaymentDAO
from src.domain.payment.dto import SumByPeriodInputDTO, SumPeriodGroupEnum
from src.domain.period.dto import PeriodDTO


async def sum_by_period(incoming_text: str) -> Text:
    try:
        input_data = SumByPeriodInputDTO.model_validate_json(incoming_text)
        period = PeriodDTO.validate_from_input(
            from_dt=input_data.dt_from,
            to_dt=input_data.dt_upto
        )
    except (ValidationError, ValueError):
        return Text(
            'Невалидный запос. Пример запроса: ',
            '{"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}'
        )

    sum_by_period_result = await PaymentDAO().get_sum_by_period(period, SumPeriodGroupEnum(input_data.group_type))
    return Text(
        sum_by_period_result.model_dump_json()
    )
