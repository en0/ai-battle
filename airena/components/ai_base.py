from ..game_component import GameComponent
from ..vector import Vector2
from ..typing import IObjectService

from .bot_motion import BotMotion


class AiBase(GameComponent):
    """This class is excluded from the auto-injected component list.

    You should override this class and inject that subclass instead.
    """

    _bm: BotMotion

    @property
    def enemies(self):
        return self._obj.get_objects_by_tag("Tanks")

    def startup(self):
        self._bm = self.game_object[BotMotion]

    def move_forward(self):
        self._bm.move_forward()

    def move_backward(self):
        self._bm.move_backward()

    def move_left(self):
        self._bm.move_left()

    def move_right(self):
        self._bm.move_right()

    def set_focus(self, point: Vector2):
        self._bm.set_focus(point)

    def move_toword(self, point: Vector2):
        self._bm.move_toword(point)

    def clear_focus(self):
        self._bm.clear_focus()

    def fire(self):
        self._bm.fire()

    def __init__(self, obj: IObjectService):
        self._obj = obj
