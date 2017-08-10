import unittest
from pulsar import send, get_application, get_actor
from jirachi import ComposedApp


class TestComposedApp(unittest.TestCase):
    @classmethod
    async def setUpClass(cls):
        cls.monitor = ComposedApp()
        cls.app_cfg = await send('arbiter', 'run', cls.monitor)

    async def test_get_monitor(self):
        app = await get_application('jirachi')
        print(self.monitor.apps()[1].apps())
        arbiter = get_actor().get_actor('arbiter')
        self.assertTrue(app)
        self.assertTrue(arbiter)

    @classmethod
    async def tearDownClass(cls):
        for app in cls.monitor.apps():
            await send('arbiter', 'kill_actor', app.name)
        return
