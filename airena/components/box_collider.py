from pygame import draw, Rect, K_0
from typing import Callable, List, Tuple

from ..vector import Vector2
from ..typing import IGameObject, ICollider, CollisionDelegate
from ..game_component import GameComponent

from .transform import Transform


class BoxCollider(GameComponent, ICollider):

    # Leave this defined under global context
    # so we can toggle it for everything
    show_bounding_box: bool = False

    _callbacks: List[CollisionDelegate]
    _rect: Rect = None

    size: Vector2 = Vector2.zero()
    offset: Vector2 = Vector2.zero()

    def on_collision(self, callback: CollisionDelegate) -> None:
        self._callbacks.append(callback)

    def collide_rect(self, rect: Rect) -> bool:
        return self._rect.colliderect(rect)

    def collide_point(self, point: Tuple[float, float]) -> bool:
        return self._rect.collidepoint(point)

    def check_collision(self, game_object: IGameObject) -> None:
        if game_object.collider.collide_rect(self._rect):
            self._do_callbacks(game_object)

    def update(self) -> None:
        self._rect = Rect(self.offset, self.size)
        self._rect.center = self._xfr.position
        if BoxCollider.show_bounding_box:
            draw.rect(self.screen, (255, 255, 255), self._rect, 1)

    def startup(self) -> None:
        self._xfr = self.game_object[Transform]

    def _do_callbacks(self, game_object: IGameObject) -> None:
        for cb in self._callbacks:
            cb(game_object)

    def __init__(self):
        self._callbacks = []
