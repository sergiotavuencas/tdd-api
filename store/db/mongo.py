from motor.motor_asyncio import AsyncIOMotorClient

from store.core.config import settings

"""
    Necessário a utilização do " uuidRepresentation="standard" "
    para que ao inserir os dados no bd não levante erro no UUID.
"""


class MongoClient:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(
            settings.DATABASE_URL,
            uuidRepresentation="standard",
        )

    def get(self) -> AsyncIOMotorClient:
        return self.client


db_client = MongoClient()
