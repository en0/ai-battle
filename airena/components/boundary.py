import pygame
from typing import Callable, List

from ..game_component import GameComponent
from ..typing import IGameObject

from .transform import Transform


COLLISION_DELEGATE = Callable[[IGameObject], None]

class Boundary(GameComponent):

    _callbacks: List[COLLISION_DELEGATE]

    _rect: pygame.Rect = None
    _xfr: Transform = None

    collidable: bool = False
    height: float = None
    width: float = None

    def get_rect(self):
        self._rect.center = self._xfr.position
        return self._rect.copy()

    def check_collision(self, game_object: IGameObject):
        if not self.collidable:
            return
        if Boundary not in game_object:
            return
        if not game_object[Boundary].collidable:
            return
        if self.get_rect().colliderect(game_object[Boundary].get_rect()):
            for cb in self._callbacks:
                cb(game_object)

    def add_callback(self, callback: COLLISION_DELEGATE) -> None:
        self._callbacks.append(callback)

    def startup(self):
        self._xfr = self.game_object[Transform]
        if self.height is None:
            raise RuntimeError("Boundary requires attribute height.")
        if self.width is None:
            raise RuntimeError("Boundary requires attribute width.")
        self._rect = pygame.Rect(0, 0, self.width, self.height)

    def update(self):
        self._rect.center = self._xfr.position

    def __init__(self):
        self._callbacks = []
