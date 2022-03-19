import math
import pygame
from typing import Optional

from ..typing import IDisplayService
from ..game_component import GameComponent

from .transform import Transform


class BulletRenderer(GameComponent):

    _gfx: IDisplayService
    _xfr: Optional[Transform] = None

    radius = 3
    color = (255, 0, 0)

    def update(self) -> None:
        x, y = self._xfr.position - (self.radius*2)
        pygame.draw.circle(self._gfx, self.color, self._xfr.position, self.radius)

    def startup(self) -> None:
        self._xfr = self.game_object[Transform]

    def __init__(self, gfx: IDisplayService):
        self._gfx = gfx
