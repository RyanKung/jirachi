from pulsar.apps import MultiApp
from pulsar.apps.wsgi.handlers import WsgiHandler
from pulsar.apps.wsgi import WSGIServer
from jirachi.core import wsgi
from jirachi.io import RequestMonitor
from jirachi.io import SchedulerMonitor

__all__ = ['wsgi', 'ComposedApp', 'ComposedIO',
           'RequestMonitor', 'SchedulerMonitor']


__version__ = '0.1.2.5'


class ComposedIO(MultiApp):
    name = 'io'

    def build(self):
        yield self.new_app(RequestMonitor, worker=10)
        yield self.new_app(SchedulerMonitor, worker=10)


class ComposedApp(MultiApp):
    name = 'jirachi'

    def build(self):
        yield self.new_app(WSGIServer, callable=WsgiHandler((wsgi, )),)
        yield self.new_app(ComposedIO, worker=10)
