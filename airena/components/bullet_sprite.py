from pygame import draw
from ..vector import Vector2
from ..typing import IDisplayService
from ..game_component import GameComponent
from .transform import Transform


class BulletSprite(GameComponent):

    _xfr: Transform = None

    color = (255, 255, 255)

    def startup(self) -> None:
        self._xfr = self.game_object[Transform]

    def update(self) -> None:
        draw.polygon(self._gfx, self.color, self._compute_poly())
        draw.circle(self._gfx, self.color, self._xfr.position, 3)

    def _compute_poly(self):
        top_left = Vector2(-3, -10).rotate(self._xfr.rotation) + self._xfr.position
        top_right = Vector2(-3, -1).rotate(self._xfr.rotation) + self._xfr.position
        bottom_left = Vector2(3, -10).rotate(self._xfr.rotation) + self._xfr.position
        bottom_right = Vector2(3, -1).rotate(self._xfr.rotation) + self._xfr.position
        return [top_left, top_right, bottom_right, bottom_left]

    def __init__(self, gfx: IDisplayService) -> None:
        self._gfx = gfx

