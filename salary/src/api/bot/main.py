from src.api.bot.loader import dp
from src.api.bot import main_router
from src.database.mongo.model import init_models


async def on_startup():
    await init_models()


dp.include_router(main_router)

dp.startup.register(on_startup)
