from pulsar import get_application, get_actor, send
from pulsar.apps import Application
from itertools import count
from random import randint


__all__ = ['JirachiMonitor', 'JirachiMonitorNotFound']


class JirachiWorkerNotFound(Exception):
    pass


class JirachiMonitorNotFound(Exception):
    pass


class JirachiMonitor(Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def monitor_start(self, monitor, exec=None):
        monitor.counter = count(0)

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
    async def get_worker(cls, monitor):
        workers = {id: actor
                   for id, actor in monitor.managed_actors.items()
                   if actor.info}
        if workers:
            if not monitor.counter:
                index = randint(0, len(workers) - 1)
            else:
                index = next(monitor.counter) % len(workers)
            wid = list(workers.keys())[index]
            worker = get_actor().get_actor(wid)
            return worker
        raise JirachiWorkerNotFound(
            {k: v.__dict__ for k, v in monitor.managed_actors.items()})

    @classmethod
    async def kill(cls):
        monitor = await cls.get_monitor()
        return await send('arbiter', 'kill_actor', monitor.name)
