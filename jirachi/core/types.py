from typing import Union, Callable, Generic, GenericMeta, TypeVar

from types import CoroutineType
from pulsar.apps.wsgi import WsgiResponse, WsgiRequest

__all__ = ['Request', 'Response',
           'MaybeCorouteine', 'Handler',
           'MaybeType', 'Maybe']


Request = WsgiRequest
Response = WsgiResponse

MaybeCorouteine = Union[CoroutineType, Callable]
Handler = Callable[..., WsgiResponse]


MaybeType = Generic[TypeVar("Just"), TypeVar("Error")]
Maybe: GenericMeta = type("Maybe", (MaybeType, ), {})
