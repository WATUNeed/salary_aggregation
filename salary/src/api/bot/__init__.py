import aiogram

from src.api.bot.commands.payments import payments_router
from src.api.bot.commands.start import start_router

main_router = aiogram.Router()

main_router.include_routers(start_router, payments_router)
