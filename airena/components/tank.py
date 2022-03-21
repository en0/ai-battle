from math import cos, sin, atan2, pi
from typing import Dict, Any

from ..presets import bullet_preset
from ..game_component import GameComponent
from ..typing import IClockService, IObjectService, IGameObject
from ..vector import Vector2

from .transform import Transform
from .tank_sprite import TankSprite
from .box_collider import BoxCollider
from .meta import Meta


class Tank(GameComponent):

    _props: Dict[str, Any]
    _xfr: Transform = None
    _spr: TankSprite
    _fire_bullet = False
    _next_fire_ts = 0
    _movement_vector = Vector2.zero()
    _turn_vector = 0
    _hat_turn_vector = 0

    @property
    def can_fire(self) -> bool:
        return self.now_ms >= self._next_fire_ts

    def fire(self) -> None:
        if self.can_fire:
            self._fire_bullet = True

    def turn_hat(self, direction: float) -> None:
        self._hat_turn_vector = -1 if direction < 0 else 1 if direction > 0 else 0

    def turn(self, direction: float) -> None:
        self._turn_vector = -1 if direction < 0 else 1 if direction > 0 else 0

    def move(self, direction: float) -> None:
        self._movement_vector = (
            -Vector2.from_rotation(self._xfr.rotation) if direction < 0
            else Vector2.from_rotation(self._xfr.rotation) if direction > 0
            else Vector2.zero()
        )

    def update(self) -> None:
        self._do_fire()
        self._do_turn()
        self._do_hat_turn()
        self._do_move()

    def startup(self) -> None:
        self._props = self.game_object[Meta].props
        self._xfr = self.game_object[Transform]
        self._spr = self.game_object[TankSprite]
        self._box = self.game_object[BoxCollider]
        self._box.on_collision(self._do_collision)

    def _do_collision(self, go: IGameObject):
        if go[Meta].type == "Bullet":
            self._props["health"] -= go[Meta].props["damage"]
            if self._props["health"] <= 0:
                self.kill_object(self.game_object)

    def _do_fire(self) -> None:
        if self.can_fire and self._fire_bullet:

            bullet_position = Vector2.from_rotation(
                self._props["hat_rotation"],
                self._props["barrel_length"] + 25
            ) + self._xfr.position

            self._fire_bullet = False
            self._next_fire_ts = self.now_ms + self._props["fire_cooldown"]
            self.spawn_object(bullet_preset(
                position=bullet_position,
                rotation=self._props["hat_rotation"],
                vector=Vector2.from_rotation(self._props["hat_rotation"]),
                speed=self._props["bullet_speed"],
                color=self._spr.color), self.game_object)

    def _do_turn(self) -> None:
        turn_speed = self._props["turn_speed"]
        rotation = self._turn_vector * turn_speed * self.frame_delay
        self._xfr.rotation += rotation
        self._props["hat_rotation"] += rotation
        self._turn_vector = 0

    def _do_hat_turn(self) -> None:
        turn_speed = self._props["turn_speed"]
        rotation = self._hat_turn_vector * turn_speed * self.frame_delay
        self._props["hat_rotation"] += rotation
        self._hat_turn_vector = 0

    def _do_move(self) -> None:
        move_speed = self._props["movement_speed"]
        vector = self._movement_vector * move_speed * self.frame_delay
        self._xfr.position += vector
        self._movement_vector = 0

