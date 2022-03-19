from typing import Optional
from math import acos, atan2, cos, sin, pi

from ..game_component import GameComponent
from ..vector import Vector2
from ..typing import IClockService, IObjectService, IDisplayService, IGameObject

from .transform import Transform
from .tank_renderer import TankRenderer
from .boundary import Boundary


class BotMotion(GameComponent):

    _xfr: Optional[Transform] = None
    _turn_to_target: Optional[Vector2] = None
    _move_to_target: Optional[Vector2] = None
    _move_vector: Optional[Vector2] = Vector2.zero()
    _fire_bullet = False
    _next_fire_time = 0

    fire_cooldown: int = 500
    bullet_speed: float = 400
    turn_speed: float = 2
    move_speed: float = 100

    def fire(self) -> None:
        self._fire_bullet = True

    def set_focus(self, point: Vector2) -> None:
        self._turn_to_target = point

    def clear_focus(self) -> None:
        self._turn_to_target = None

    def move_toword(self, point: Vector2) -> None:
        self._move_to_target = point

    def move_forward(self) -> None:
        self._move_vector += self._get_facing_vector()

    def move_backward(self) -> None:
        self._move_vector += self._get_facing_vector(pi)

    def move_left(self) -> None:
        self._move_vector += self._get_facing_vector(-pi/2)

    def move_right(self) -> None:
        self._move_vector += self._get_facing_vector(pi/2)

    def has_focus(self) -> None:
        return self._turn_to_target is not None

    def has_move_toward_target(self) -> bool:
        return self._move_to_target is not None

    def update(self) -> None:
        self._xfr.rotation += self._get_angular_velocity()
        new_position = self._xfr.position + self._get_forward_velocity()
        if self._world_border.collidepoint(new_position):
            self._xfr.position = new_position
        self._move_vector = Vector2.zero()
        self._fire_maybe()

    def startup(self) -> None:
        self._xfr = self.game_object[Transform]
        self._rdr = self.game_object[TankRenderer]
        self._brd = self.game_object[Boundary]
        self._brd.add_callback(self._on_collision)

    def _on_collision(self, go: IGameObject):
        if self.game_object == go.owner:
            return
        if go.tag == "Bullet":
            self._obj.kill(self.game_object)

    def _fire_maybe(self):
        if not self._fire_bullet:
            return
        if self._clk.now_ms < self._next_fire_time:
            return
        self._fire_bullet = False
        self._obj.spawn("Bullet", {
            "BulletRenderer": {"color": self._rdr.color},
            "Motion": {"vector": self._get_facing_vector(), "speed": self.bullet_speed},
            "Transform": {"position": self._xfr.cast_ray(self._rdr.barrel)},
            "Boundary": {"width": 10, "height": 10, "collidable": True}
        }, self.game_object)

        self._next_fire_time = self._clk.now_ms + self.fire_cooldown


    def _get_angular_velocity(self) -> float:
        # TODO: I think this is overly complex but i have spent to much time on it.
        # Revisit this with fresh eyes

        if self._turn_to_target is None:
            return 0

        target_v = self._turn_to_target - self._xfr.position
        facing_v = self._xfr.facing - self._xfr.position
        facing_v = self._get_facing_vector()

        mag_v = facing_v.magnitude() * target_v.magnitude()

        if mag_v == 0:
            return 0

        try:
            radians = acos(max(-1, min(1, facing_v * target_v / mag_v)))
        except ValueError:
            print("NOT AGAIN!!!!")
            print(facing_v, target_v, mag_v, facing_v * target_v / mag_v)
            raise

        if atan2(*target_v) - atan2(*(target_v - facing_v)) < 0:
            return max(-self.turn_speed * self._clk.frame_delay, -radians)
        else:
            return min(self.turn_speed * self._clk.frame_delay, radians)

    def _get_forward_velocity(self) -> Vector2:
        if self._move_to_target:
            target_v = (self._move_to_target - self._xfr.position)
            target_v_n = target_v.normalize()
            if target_v.magnitude() < target_v_n.magnitude():
                self._move_to_target = None
                return target_v
            return (target_v_n * self._clk.frame_delay * self.move_speed)

        ret = self._move_vector
        self._move_vector = Vector2.zero()
        return ret.normalize() * self._clk.frame_delay * self.move_speed

    def _get_facing_vector(self, adj: float = 0) -> Vector2:
        return Vector2(
            cos(self._xfr.rotation + adj),
            sin(self._xfr.rotation + adj),
        )

    def __init__(self, clock: IClockService, obj: IObjectService, gfx: IDisplayService) -> None:
        self._clk = clock
        self._obj = obj
        self._world_border = gfx.get_rect()

