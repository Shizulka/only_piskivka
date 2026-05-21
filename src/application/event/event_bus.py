
from collections import defaultdict
from typing import Callable, Type, Any


class EventBus:
    def __init__(self):
        self.subscribers = defaultdict(list)

    def subscribe(self, event_type: Type, handler: Callable):
        self.subscribers[event_type].append(handler)

    def publish(self, event: Any):
        print(f"EVENT PUBLISHED: {type(event).__name__}")
        for handler in self.subscribers[type(event)]:
            try:
                handler(event)
            except Exception:
                pass