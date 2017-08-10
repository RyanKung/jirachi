from pulsar import send
from motor.motor_asyncio import AsyncIOMotorClient
from jirachi.io.abstract import MongoDBMonitor

__all__ = ['MongoDBMonitor']


class MongoDBMonitor(MongoDBMonitor):
    name = "mongodb"

    async def monitor_start(self, monitor, exec=None):
        monitor.client = await AsyncIOMotorClient(self.cfg.mongoconf)

    async def _insert_one(actor, db, collect, data):
        return await actor[db][collect].insert_one(data)

    async def _find_one(actor, db, collect, data):
        return await actor[db][collect].find_one(data)

    @classmethod
    async def insert_one(cls, db: str, collect: str, data: dict) -> dict:
        monitor = await cls.get_monitor()
        return await send(monitor, 'run', cls._insert_one, db, collect, data)

    @classmethod
    async def find_one(cls, db: str, collect: str, data: dict) -> dict:
        monitor = await cls.get_monitor()
        return await send(monitor, 'run', cls._find_one, db, collect, data)
