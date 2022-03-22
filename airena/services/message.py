import pygame
from typing import Callable, Iterable, Any

from ..typing import IMessageService, CallbackDelegate, FilterDelegate


class MessageService(IMessageService):

    def register_callback(
        self,
        event_type: int,
        callback: CallbackDelegate,
        predicate: FilterDelegate = None
    ):
        type_callbacks = self._callbacks.setdefault(event_type, set())
        type_callbacks.add((callback, predicate or (lambda x: True)))

    def unregister_callback(self, callback: CallbackDelegate):
        to_remove = []
        for t, callbacks in self._callbacks.items():
            for c, p in callbacks:
                if callback == c:
                    to_remove.append((t, c, p))
        for t, c, p in to_remove:
            self._callbacks[t].remove((c, p))

    def broadcast(self, name: str, **data):
        event = pygame.event.Event(pygame.USEREVENT, name=name, **data)
        pygame.event.post(event)

    def update(self, events: Iterable[pygame.event.Event]):
        for event in events:
            for callback, predicate in self._callbacks.get(event.type, []):
                if predicate(event):
                    callback(event)

    def __init__(self):
        self._callbacks = {}
