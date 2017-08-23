from pulsar import get_application, get_actor, send
from pulsar.apps import Application
from random import randint


__all__ = ['JirachiMonitor', 'JirachiMonitorNotFound']


class JirachiMonitorNotFound(Exception):
    pass


class JirachiMonitor(Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    async def get_arbiter(cls):
        arbiter = get_actor().get_actor('arbiter')
        return arbiter

    @classmethod
    async def get_monitor(cls):
        async def get_monitor_via_arbiter():
            arbiter = get_actor().get_actor('arbiter')
            monitor_name = next(
                (m for m in arbiter.monitors if cls.name in m), None)
            monitor = await get_application(monitor_name)
            return monitor
        name = cls.cfg.name or cls.name
        monitor = get_actor().get_actor(name)
        return monitor or await get_monitor_via_arbiter()

    @classmethod
    async def get_worker(cls, monitor=None):

        if not monitor:
            monitor = await cls.get_monitor()
        workers = monitor.managed_actors
        if workers:
            index = randint(0, len(workers) - 1)
            wid = list(workers.keys())[index]
            worker = get_actor().get_actor(wid)
        return worker

    @classmethod
    async def kill(cls):
        monitor = await cls.get_monitor()
        return await send('arbiter', 'kill_actor', monitor.name)
