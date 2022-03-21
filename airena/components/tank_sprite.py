from pygame import draw, Rect
from typing import Dict, Any

from ..typing import IDisplayService
from ..game_component import GameComponent
from ..vector import Vector2

from .transform import Transform
from .meta import Meta


class TankSprite(GameComponent):

    _props: Dict[str, Any]

    _gfx: IDisplayService = None
    _xfr: Transform = None

    color = (255, 255, 255)

    def update(self) -> None:

        # body
        draw.polygon(
            self._gfx,
            self.color,
            self._compute_poly(),
            self._props["body_thinkness"]
        )

        # Hat
        draw.circle(
            self._gfx,
            self.color,
            self._xfr.position,
            self._props["hat_radius"])

        # Barrel
        draw.line(
            self._gfx,
            self.color,
            self._xfr.position,
            Vector2.from_rotation(
                self._props["hat_rotation"],
                self._props["hat_radius"] * self._props["barrel_length"]
            ) + self._xfr.position,
            self._props["barrel_thinkness"])

        h = 40 * (self._props["health"] / 100) - 20
        draw.line(
            self._gfx,
            self.color,
            self._xfr.position - Vector2(-h, -35),
            self._xfr.position - Vector2(20, -35),
            3)

    def startup(self) -> None:
        self._props = self.game_object[Meta].props
        self._xfr = self.game_object[Transform]

    def _compute_poly(self):
        bl = self._props["body_length"]
        bw = self._props["body_width"]
        top_left = Vector2(-bw, -bl).rotate(self._xfr.rotation) + self._xfr.position
        top_right = Vector2(-bw, bl).rotate(self._xfr.rotation) + self._xfr.position
        bottom_left = Vector2(bw, -bl).rotate(self._xfr.rotation) + self._xfr.position
        bottom_right = Vector2(bw, bl).rotate(self._xfr.rotation) + self._xfr.position
        return [top_left, top_right, bottom_right, bottom_left]

    def __init__(self, gfx: IDisplayService):
        self._gfx = gfx
