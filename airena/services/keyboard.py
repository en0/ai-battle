import pygame
from typing import List, Callable, Optional, Iterable

from ..typing import IMessageService, IKeyboardService, KbCallbackDelegate


class KeyboardService(IKeyboardService):

    def register_callback(
        self,
        key: int,
        keydown_callback: Optional[KbCallbackDelegate] = None,
        keyup_callback: Optional[KbCallbackDelegate] = None,
    ):

        if keydown_callback:
            self._bus.register_callback(
                pygame.KEYDOWN,
                self._wrap_callback(keydown_callback),
                lambda e: key == e.key)

        if keyup_callback:
            self._bus.register_callback(
                pygame.KEYUP,
                self._wrap_callback(keyup_callback),
                lambda e: key == e.key)

    def unregister_callback(self, callback: KbCallbackDelegate) -> None:
        if callback not in self._reverse_lookup:
            return
        for _cb in self._reverse_lookup.pop(callback, []):
            self._bus.unregister_callback(_cb)

    def unregister_callbacks(self, callbacks: Iterable[KbCallbackDelegate]) -> None:
        for _cb in callbacks:
            self.unregister_callback(_cb)

    def _wrap_callback(self, callback: KbCallbackDelegate):
        _callback = lambda e: callback(e.type, e.key, e.mod)
        self._reverse_lookup.setdefault(callback, []).append(_callback)
        return _callback

    def __init__(self, bus: IMessageService):
        self._bus = bus
        self._reverse_lookup = {}

