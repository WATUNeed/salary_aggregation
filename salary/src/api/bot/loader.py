from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.config.bot import BOT_CONFIG


storage = MemoryStorage()

bot = Bot(**BOT_CONFIG.get_bot_attributes())
dp = Dispatcher(storage=storage)