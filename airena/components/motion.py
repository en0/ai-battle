from typing import Optional
from ..game_component import GameComponent
from ..lib import Vector2
from ..typing import IClockService, IDisplayService, IObjectService

from .transform import Transform


class Motion(GameComponent):

    _xfr: Optional[Transform] = None

    vector: Optional[Vector2] = None
    speed: float = 0

    def update(self) -> None:
        self._xfr.position += self.vector * self._clk.frame_delay * self.speed
        if not self._boundary.collidepoint(self._xfr.position):
            # Just for safty reasons
            self._obj.kill(self.game_object)

    def startup(self) -> None:
        self._xfr = self.game_object[Transform]

    def __init__(self, clock: IClockService, gfx: IDisplayService, obj: IObjectService) -> None:
        self._clk = clock
        self._boundary = gfx.get_rect()
        self._obj = obj

