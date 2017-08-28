from typing import Iterable
import asyncpg
from asyncpg import Record
from asyncpg.exceptions import InterfaceError
from pulsar import send
from jirachi.io.abstract import JirachiMonitor, JirachiWorkerNotFound
import traceback


__all__ = ['PostgresMonitor']


class PostgresMonitor(JirachiMonitor):
    name = "postgres"

    async def connect(self, *args, **kwargs):
        return await asyncpg.connect(**self.cfg.pgconfigs)

    @staticmethod
    async def _execute(actor, sql) -> str:
        return await actor.conn.execute(sql)

    @classmethod
    async def _fetchrow(cls, actor, sql) -> dict:
        if actor.is_monitor and actor.managed_actors:
            try:
                worker = await cls.get_worker(monitor=actor)
                return await send(worker, 'run', cls._fetchrow, sql)
            except JirachiWorkerNotFound:
                traceback.print_exc()
        try:
            res = await actor.conn.fetchrow(sql)
        except InterfaceError:
            traceback.print_exc()
            res = await cls.fetch(sql)
        return dict(res)

    @classmethod
    async def _fetch(cls, actor, sql) -> dict:

        if actor.is_monitor and actor.managed_actors:
            try:
                worker = await cls.get_worker(monitor=actor)
                return await send(worker, 'run', cls._fetch, sql)
            except JirachiWorkerNotFound:
                traceback.print_exc()
        try:
            res = await actor.conn.fetch(sql)
        except InterfaceError:
            traceback.print_exc()
            res = await cls.fetch(sql)
        return list(map(dict, res))

    @classmethod
    async def _transaction(cls, actor, sqls) -> str:
        if actor.is_monitor and actor.managed_actors:
            try:
                worker = await cls.get_worker(monitor=actor)
                return await send(worker, 'run', cls._transaction, sqls)
            except JirachiWorkerNotFound:
                traceback.print_exc()
        try:
            async with actor.conn.transaction():
                res = [await actor.conn.execute(s) for s in sqls]
        except InterfaceError as e:
            traceback.print_exc()
            res = await cls.transaction(sqls)
        return res

    async def monitor_start(self, monitor, exec=None):
        await super().monitor_start(monitor, exec)
        monitor.conn = await asyncpg.connect(**self.cfg.pgconf)

    async def monitor_stopping(self, monitor, exec=None):
        if hasattr(monitor, 'conn'):
            monitor.conn.terminate()

    async def worker_start(self, worker, exc=None):
        if not worker.is_arbiter or worker.is_monitor:
            worker.conn = await asyncpg.connect(**self.cfg.pgconf)

    async def worker_stopping(self, worker, exc=None):
        if not worker.is_arbiter or worker.is_monitor:
            if hasattr(worker, 'conn'):
                worker.conn.terminate()

    @classmethod
    async def execute(cls, sql: str) -> str:
        monitor = await cls.get_monitor()
        return await send(monitor, 'run', cls._execute, sql)

    @classmethod
    async def fetch(cls, sql: str) -> Record:
        monitor = await cls.get_monitor()
        return await send(monitor, 'run', cls._fetch, sql)

    @classmethod
    async def fetchrow(cls, sql: str) -> Record:
        monitor = await cls.get_monitor()
        return await send(monitor, 'run', cls._fetchrow, sql)

    @classmethod
    async def transaction(cls, sqls: Iterable[str]) -> str:
        monitor = await cls.get_monitor()
        return await send(monitor, 'run', cls._transaction, sqls)
