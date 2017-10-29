from jirachi.io.abstract import JirachiMonitor


class RabbitMQMonitor(JirachiMonitor):
    namee = 'rabbitmq'

    def push_to_queue(self):
        pass

    def queue_decorator(self):
        pass

    async def monitor_start(self, monitor, exec=None):
        await super().monitor_start(monitor, exec)

    async def monitor_stopping(self, monitor, exec=None):
        pass
