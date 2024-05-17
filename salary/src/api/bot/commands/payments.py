import json

import aiogram
from aiogram.types import Message
from pydantic import ValidationError

from src.domain.payment.dal import PaymentDAO
from src.domain.payment.dto import PaymentSumForPeriodDTO, PaymentGroupEnum
from src.domain.period.dto import PeriodDTO

payments_router = aiogram.Router(name='payments')


@payments_router.message()
async def payments_sum_for_period_by_group_type_command(message: Message):
    try:
        input_data = PaymentSumForPeriodDTO.model_validate_json(message.text)
    except ValidationError:
        answer = ('Невалидный запос. '
                  'Пример запроса: '
                  '{"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}')
        return await message.reply(answer)
    period = PeriodDTO(
        from_dt=input_data.dt_from,
        to_dt=input_data.dt_upto
    )
    result = await PaymentDAO().get_sum_for_period_by_group_type(period, PaymentGroupEnum(input_data.group_type))
    await message.answer(f'{result}')