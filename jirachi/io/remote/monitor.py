from hashlib import sha1
import time
import json
from pulsar import get_actor, Future
from pulsar.apps.wsgi import WSGIServer, WsgiResponse, WsgiHandler
import aio_etcd as etcd
from jirachi.io.abstract import JirachiMonitor, JirachiMonitorNotFound
from pulsar.apps.wsgi import Router

__all__ = ['RemoteMonitorWSGI']

blueprint = Router('/')


@blueprint.router('/remote/<string:monitor>/event/<string:event>/', methods=['post'])
async def remote_wsgi(request):
    hash_code = sha1(str(time.time()).encode()).hexdigest()
    monitor_name = request.urlargs['monitor']
    event_name = request.urlargs['event']
    data = request.body_data

    actor = get_actor()
    monitor = actor.get_actor(monitor_name)
    if monitor:
        monitor.fire_event(event_name, data)
    elif not (actor.is_arbiter() or actor.is_monitor() and actor.monitor == monitor):
        actor.monitor.fire_event(event_name, msg=data)
    else:
        raise JirachiMonitorNotFound('Cant found Monitor %s' % monitor)
    return WsgiResponse(200, json.dumps({
        'successed': True,
        'token': hash_code
    }))


class RemoteMonitorWSGI(WSGIServer, JirachiMonitor):
    name = 'remote_monitor'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cfg.callable = WsgiHandler((blueprint, ))
        if not hasattr(self.cfg, 'blacklist'):
            self.cfg.blacklist = []

    @staticmethod
    async def singlecast(msg, actor_name):
        actor = get_actor()
        if not actor.name == actor_name:
            actor = actor.get_actor(actor_name)
        if not actor and actor.monitor.name == actor.name:
            actor = actor.monitor
        actor.fire_event('singlecast', msg)
        actor.future = Future()
        return actor.future

    @staticmethod
    def event_test(msg):
        print('test event %s' % msg)

    async def monitor_start(self, monitor, exec=None):
        monitor.bind_event('test', self.event_test)
        if not hasattr(self.cfg, 'etcdconf'):
            monitor.etcd = etcd.Client()
        else:
            monitor.etcd = etcd.Client(**self.cfg.etcdconf)
        await super().monitor_start(monitor)

    async def worker_start(self, worker, *args, **kwargs):
        worker.bind_event('test', self.event_test)

    async def search_remote(self):
        pass

    async def sync_remote(self):
        pass
