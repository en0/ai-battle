import math
import pygame
from typing import Optional

from ..typing import IDisplayService
from ..game_component import GameComponent

from .transform import Transform


class TankRenderer(GameComponent):

    _gfx: IDisplayService
    _xfr: Optional[Transform] = None

    radius = 10
    color = (255, 0, 0)
    barrel = 3
    width = 0
    line_width = 6

    def update(self) -> None:
        x, y = self._xfr.position - (self.radius*2)
        pygame.draw.circle(self._gfx, self.color, self._xfr.position, self.radius, self.width)
        pygame.draw.line(self._gfx, self.color, self._xfr.position, self._xfr.cast_ray(self.radius * self.barrel), self.line_width)
        pygame.draw.rect(self._gfx, self.color, pygame.Rect(x, y, self.radius*4, self.radius*4), 1)

    def startup(self) -> None:
        self._xfr = self.game_object[Transform]

    def __init__(self, gfx: IDisplayService):
        self._gfx = gfx
