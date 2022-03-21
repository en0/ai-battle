from typing import Dict, Any
from math import cos, sin
from ..game_component import GameComponent
from ..vector import Vector2


class Transform(GameComponent):

    position: Vector2 = Vector2(0, 0)
    rotation: float = 0

    def startup(self):
        # incase the preset didn't use a complete vector2
        self.position = Vector2(*self.position)
