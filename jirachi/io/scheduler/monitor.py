import time
from functools import wraps
from jirachi.io.abstract import JirachiMonitor

__all__ = ['SchedulerMonitor']


class SchedulerMonitor(JirachiMonitor):
    name = 'scheduler_worker'
    _tasks = []

    def task(self, fn, rule=lambda t: int(t) % 1 == 0):
        self._tasks.append([rule, fn])

        @wraps(fn)
        def _(*args, **kwargs):
            return fn(*args, **kwargs)
        return _

    def monitor_task(self, monitor):
        [t[1]() for t in self._tasks if t[0](time.time())]
