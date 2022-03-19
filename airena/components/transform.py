from math import cos, sin
from ..game_component import GameComponent
from ..lib import Vector2


class Transform(GameComponent):

    position = Vector2(0, 0)
    rotation = 0
    scale = 1

    @property
    def facing(self) -> Vector2:
        return Vector2(
            cos(self.rotation),
            sin(self.rotation),
        ) + self.position

    def cast_ray(self, distance: float) -> Vector2:
        return Vector2(
            cos(self.rotation) * distance,
            sin(self.rotation) * distance,
        ) + self.position

    def startup(self):
        # incase the preset didn't use a complete vector2
        self.position = Vector2(*self.position)

