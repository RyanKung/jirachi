from pulsar.apps import Application
from pulsar import arbiter, ensure_future, get_actor, send


class TestApp(Application):
    def monitor_start(self, monitor, exc=None):
        print('monitor %s start' % monitor.name)
        monitor.bind_event('hello_monitor', print)

    async def worker_start(self, worker, exc=None):
        print('worker %s start' % worker.name)
        worker.bind_event('hello_worker', print)
        await send(worker.monitor, 'run', self.fire, 'cmd', 'test fire')

    def worker_info(self, worker, info=None):
        print('worker %s info' % worker.name)

    @staticmethod
    def fire(monitor, cmd, data, **kw):
        monitor.fire_event('hello_monitor', data)
        print(monitor.managed_actors)


async def main(arbiter, **kw):
    app = TestApp(workers=2)
    res = ensure_future(app(arbiter))
    res.add_done_callback(play_with_monitor)


def play_with_monitor(m):
    monitor = get_actor().get_actor('testapp')
    assert monitor is not None
    monitor.fire_event('hello_monitor', 'hello monitor')
    print(monitor.managed_actors)


if __name__ == '__main__':
    arbiter(start=main).start()
