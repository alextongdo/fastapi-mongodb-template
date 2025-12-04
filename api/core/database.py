from beanie import init_beanie
from pymongo import AsyncMongoClient

import api.src.models as models
from api.core.config import settings

client = AsyncMongoClient(settings.MONGO_URI)

def get_client():
    return client

async def init_db():
    client = get_client()
    await init_beanie(
        database=client[settings.MONGO_DB_NAME],
        document_models=models.__all__,
    )
    await client[settings.MONGO_DB_NAME].command('ping')

async def drop_db():
    client = get_client()
    await client.drop_database(settings.MONGO_DB_NAME)

async def drop_collections():
    client = get_client()
    db = client[settings.MONGO_DB_NAME]
    collection_names = await db.list_collection_names()
    for collection_name in collection_names:
        await db[collection_name].drop()