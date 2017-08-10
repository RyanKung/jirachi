from typing import Callable, Any
import json
from functools import wraps
from asyncio import coroutine
from jirachi.core.wsgi import success_response, error_response
from jirachi.core.types import (MaybeCorouteine, Handler,
                                Response, Maybe)
from asyncio import iscoroutinefunction


__all__ = ['maybe_coroutine', 'maybe_async_cps', 'jsonrpc']


def maybe_coroutine(fn: Callable) -> Callable[..., MaybeCorouteine]:
    if iscoroutinefunction(fn):
        return coroutine
    else:
        return lambda x: x


def maybe_async_cps(fn: Callable) -> MaybeCorouteine:

    def parted(context: Callable[[Maybe], Response]):
        @wraps(fn)
        @maybe_coroutine(fn)
        def _(*args, **kwargs):
            try:
                if iscoroutinefunction(fn):
                    result = yield from fn(*args, **kwargs)
                else:
                    result = fn(*args, **kwargs)
            except Exception as e:
                result = e
            return context(result)
        return _
    return parted


def jsonrpc(fn: Callable) -> Handler:
    def error(e: Exception) -> Response:
        res = dict(result=None, error=e.args, id=1)
        return error_response(json.dumps(res).encode())

    def just(r: dict) -> Response:
        res = dict(result=r, error=None, id=1)
        return success_response(json.dumps(res).encode())

    @maybe_async_cps(fn)
    def handler(res: Maybe[Any, Exception]) -> Response:
        if isinstance(res, Exception):
            return error(res)
        else:
            return just(res)

    return handler
