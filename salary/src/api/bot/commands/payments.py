import aiogram
from aiogram.types import Message

from src.domain.payment.service import sum_by_period

payments_router = aiogram.Router(name='payments')


@payments_router.message()
async def payments_sum_by_period_command(message: Message):
    context = await sum_by_period(message.text)
    await message.answer(**context.as_kwargs())
