from functools import partial
import unittest
from pulsar import send
from pulsar import Config
from jirachi.io.scheduler import SchedulerMonitor
import asyncio

monitor = SchedulerMonitor(workers=1, name='scheduler_worker')

res = []


@partial(monitor.task, rule=lambda t: int(t) % 1 == 0)
def task():
    res.append('a')


class TestScheduler(unittest.TestCase):
    @classmethod
    async def setUpClass(cls):
        await send('arbiter', 'run', monitor)

    @classmethod
    def tearDownClass(cls):
        return send('arbiter', 'kill_actor', 'scheduler_worker')

    async def testMeta(self):
        await asyncio.sleep(5)
        self.assertTrue(res)
