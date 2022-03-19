from pygame.time import Clock as _Clock
from time import time
from ..typing import IClockService


class ClockService(IClockService):

    _delta: int

    @property
    def frame_delay(self) -> float:
        return self._delta / 1000

    @property
    def frame_delay_ms(self) -> int:
        return self._delta

    @property
    def frame_rate(self) -> float:
        return self._c.get_fps()

    @property
    def now_ms(self) -> int:
        return int(time() * 1000)

    @property
    def now(self) -> float:
        return time()

    def update(self, framerate: int):
        self._delta = self._c.tick(framerate)

    def __init__(self):
        self._c = _Clock()
        self._delta = self._c.tick()
