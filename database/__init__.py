from pymongo import MongoClient
from datetime import datetime
from models import Drug
from asyncio import AbstractEventLoop
from motor.motor_asyncio import AsyncIOMotorClient
from logging import getLogger

logger = getLogger('pdxfda')


class Client(MongoClient):
    """Represents the connection to MongoDB."""

    def is_rejected(self, drug_id: str) -> bool:
        """Checks if a drug has been previously rejected"""
        print(type(self.PDXFDA.Drugs.find_one(filter={"drug_id": drug_id})))

    def get_keywords(self):
        return [doc["keyword"] for doc in list(self.PDXFDA.Keywords.find())]

    def update_drug(self, _data):
        data = {'$set': _data}
        self.PDXFDA.Drugs.update_one({'id': _data['id']}, data, upsert=True)
        logger.info(f"Adding to database: {data}")
    
    def get_rejected(self):
        return {doc['id'] for doc in self.PDXFDA.Drugs.find(filter={'rejected': True})}


class AsyncClient(AsyncIOMotorClient):
    """Async connection to MongoDB"""

    async def get_keywords(self):
        return [
            doc["keyword"] 
            for doc in await self.PDXFDA.Keywords.find().to_list(length=None)
        ]
