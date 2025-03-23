from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import MONGODB_CONNECTION_STRING

def get_mongo_client() -> AsyncIOMotorClient:
    return AsyncIOMotorClient(MONGODB_CONNECTION_STRING)