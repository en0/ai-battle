from ..typing import IClockService, IObjectService
from ..game_component import GameComponent
from ..vector import Vector2

from .transform import Transform
from .box_collider import BoxCollider


class Projectile(GameComponent):

    vector: Vector2 = Vector2.zero()
    speed: float = 0

    def startup(self) -> None:
        self.vector = self.vector.normalize() * self.speed
        self._xfr = self.game_object[Transform]
        self._box = self.game_object[BoxCollider]
        self._box.on_collision(self._destroy_projectile)

    def update(self) -> None:
        self._xfr.position += (self.vector * self._clk.frame_delay)

    def _destroy_projectile(self, *a):
        self._obj.kill(self.game_object)

    def __init__(self, clk: IClockService, obj: IObjectService) -> None:
        self._clk = clk
        self._obj = obj

