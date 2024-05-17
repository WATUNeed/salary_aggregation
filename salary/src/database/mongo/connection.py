from motor.motor_asyncio import AsyncIOMotorClient

from src.config.mongo import MONGO_CONFIG


client = AsyncIOMotorClient(MONGO_CONFIG.connection_string())
