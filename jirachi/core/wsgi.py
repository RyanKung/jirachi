from functools import partial
from typing import Callable
from pwsgi.router import BluePrint
from pulsar.apps.wsgi import WsgiResponse


__all__ = ['wsgi', 'error_response', 'success_response']


wsgi: BluePrint = BluePrint('/')
success_response: Callable = partial(WsgiResponse, 200)
error_response: Callable = partial(WsgiResponse, 500)

response = success_response
