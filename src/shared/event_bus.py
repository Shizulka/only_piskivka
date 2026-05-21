import asyncio
import inspect


class EventBus:
    def __init__(self):
        self.handlers = {}

    def subscribe(self, event_type, handler):
        if event_type not in self.handlers:
            self.handlers[event_type] = []

        self.handlers[event_type].append(handler)

    async def publish(self, event):
        event_type = type(event)

        if event_type not in self.handlers:
            return

        for handler in self.handlers[event_type]:
            if inspect.iscoroutinefunction(handler):
                asyncio.create_task(handler(event))
            else:
                result = handler(event)
                if inspect.isawaitable(result):
                    asyncio.create_task(result)


event_bus = EventBus()