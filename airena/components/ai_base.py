from abc import abstractmethod
from math import cos, sin, pi
from typing import Callable
from ..game_component import GameComponent
from ..vector import Vector2
from ..typing import IObjectService

from .bot_motion import BotMotion
from .transform import Transform


class AiBase(GameComponent):
    """This class is excluded from the auto-injected component list.

    You should override this class and inject that subclass instead.
    """

    _bm: BotMotion
    _xfr: Transform
    _update: Callable[[], None]

    @property
    def enemies(self):
        return [t for t in self._obj.get_objects_by_tag("Tank") if t is not self.game_object]

    @property
    def position(self):
        return self._xfr.position

    @property
    def rotation(self):
        return self._xfr.rotation

    @property
    def facing(self):
        return self._xfr.facing

    def has_move_to_target(self):
        return self._bm.has_move_toward_target()

    def has_focus(self):
        return self._bm.has_focus()

    def get_vector(
        self,
        rotation: float,
        dist: float,
        relative_to: Vector2 = Vector2.zero()
    ) -> Vector2:
        return Vector2(
            cos(rotation) * dist,
            sin(rotation) * dist,
        ) + relative_to

    def move_forward(self, dist: float = None):
        if dist is None:
            self._bm.move_forward()
        else:
            self.move_toword_ex(self.rotation, dist)

    def move_backward(self, dist: float = None):
        if dist is None:
            self._bm.move_backward()
        else:
            self.move_toword_ex(self.rotation - pi, dist)

    def move_left(self, dist: float = None):
        if dist is None:
            self._bm.move_left()
        else:
            self.move_toword_ex(self.rotation - (pi/2), dist)

    def move_right(self, dist: float = None):
        if dist is None:
            self._bm.move_right()
        else:
            self.move_toword_ex(self.rotation + (pi/2), dist)

    def set_focus(self, point: Vector2):
        self._bm.set_focus(point)

    def clear_focus(self):
        self._bm.clear_focus()

    def move_toword(self, point: Vector2):
        self._bm.move_toword(point)

    def move_toword_ex(self, rotation: float, dist: float):
        point = self.get_vector(rotation, dist, self.position)
        self._bm.move_toword(point)

    def fire(self):
        self._bm.fire()

    def startup(self):
        self._xfr = self.game_object[Transform]
        self._bm = self.game_object[BotMotion]

    def update(self):
        self._update()

    @abstractmethod
    def initialize(self):
        ...

    @abstractmethod
    def think(self):
        ...

    def _initialize(self):
        self._update = self.think
        self.initialize()
        self.think()

    def __init__(self, obj: IObjectService):
        self._obj = obj
        self._update = self._initialize
