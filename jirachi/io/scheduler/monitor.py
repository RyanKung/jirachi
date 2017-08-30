import time
from typing import Callable
from functools import wraps
from jirachi.io.abstract import JirachiMonitor
from asyncio import iscoroutinefunction, coroutine

__all__ = ['SchedulerMonitor']


def maybe_coroutine(fn: Callable):
    if iscoroutinefunction(fn):
        return coroutine
    else:
        return lambda x: x


class SchedulerMonitor(JirachiMonitor):
    name = 'scheduler_worker'
    _tasks = []

    def task(self, fn, rule=lambda t: int(t) % 1 == 0):
        self._tasks.append([rule, fn])

        @wraps(fn)
        @maybe_coroutine(fn)
        def _(*args, **kwargs):
            res = fn(*args, **kwargs)
            if iscoroutinefunction(fn):
                yield res
            else:
                return res
        return _

    def monitor_task(self, monitor):
        [t[1]() for t in self._tasks if t[0](time.time())]
