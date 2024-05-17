import aiogram
from aiogram.filters import CommandStart
from aiogram.types import Message

start_router = aiogram.Router(name='start')


@start_router.message(CommandStart())
async def start_command(message: Message):
    await message.reply('Hi!')
