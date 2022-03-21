from abc import abstractmethod
from typing import Callable
from ..game_component import GameComponent
from ..vector import Vector2
from ..typing import IObjectService

from .transform import Transform


class AiBase(GameComponent):
    """This class is excluded from the auto-injected component list.

    You should override this class and inject that subclass instead.
    """

    _xfr: Transform
    _update: Callable[[], None]

    @property
    def enemies(self):
        return [t for t in self._obj.get_objects_by_tag("Tank") if t is not self.game_object]

    def startup(self):
        self._xfr = self.game_object[Transform]

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
