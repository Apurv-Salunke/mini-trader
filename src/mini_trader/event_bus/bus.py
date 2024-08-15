# src/mini_trader/event_bus/bus.py

import queue
from threading import Thread
from typing import Callable, Dict, List
from .event import Event, EventType

class EventBus:
    def __init__(self):
        self._queue = queue.Queue()
        self._subscribers: Dict[EventType, List[Callable[[Event], None]]] = {}
        self._running = False
        self._thread: Thread = None

    def start(self):
        self._running = True
        self._thread = Thread(target=self._run)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join()

    def publish(self, event: Event):
        self._queue.put(event)

    def subscribe(self, event_type: EventType, callback: Callable[[Event], None]):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def unsubscribe(self, event_type: EventType, callback: Callable[[Event], None]):
        if event_type in self._subscribers and callback in self._subscribers[event_type]:
            self._subscribers[event_type].remove(callback)

    def _run(self):
        while self._running:
            try:
                event = self._queue.get(timeout=1.0)
                self._process_event(event)
            except queue.Empty:
                continue

    def _process_event(self, event: Event):
        if event.type in self._subscribers:
            for callback in self._subscribers[event.type]:
                callback(event)