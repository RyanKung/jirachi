import unittest
from pulsar import send
from jirachi.io.requests import RequestMonitor


class TestRequest(unittest.TestCase):
    @classmethod
    async def setUpClass(cls):
        cls.monitor = RequestMonitor(workers=10)
        await send('arbiter', 'run', cls.monitor)

    async def testGet(self):
        res = await RequestMonitor.request(url='http://www.baidu.com', method='GET')
        self.assertTrue(res)

    @classmethod
    def tearDownClass(cls):
        return send('arbiter', 'kill_actor', 'request_worker')
