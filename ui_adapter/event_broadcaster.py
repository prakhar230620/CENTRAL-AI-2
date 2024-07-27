import logging
from typing import List, Callable, Any
from threading import Lock

class EventBroadcaster:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.subscribers = {}
        self.lock = Lock()

    def subscribe(self, event_type: str, callback: Callable[..., Any]):
        with self.lock:
            if event_type not in self.subscribers:
                self.subscribers[event_type] = []
            self.subscribers[event_type].append(callback)
        self.logger.info(f"Subscribed to event: {event_type}")

    def unsubscribe(self, event_type: str, callback: Callable[..., Any]):
        with self.lock:
            if event_type in self.subscribers and callback in self.subscribers[event_type]:
                self.subscribers[event_type].remove(callback)
        self.logger.info(f"Unsubscribed from event: {event_type}")

    def broadcast(self, event_type: str, **kwargs):
        self.logger.info(f"Broadcasting event: {event_type}")
        with self.lock:
            if event_type in self.subscribers:
                for callback in self.subscribers[event_type]:
                    try:
                        callback(**kwargs)
                    except Exception as e:
                        self.logger.error(f"Error in event callback: {str(e)}")

    def get_subscribers(self, event_type: str) -> List[Callable[..., Any]]:
        with self.lock:
            return self.subscribers.get(event_type, [])