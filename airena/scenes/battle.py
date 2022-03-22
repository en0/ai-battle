import pygame
from typing import Set
from ..typing import IGameObject
from ..game_scene import GameScene
from ..presets import tank_preset, camera_preset

from ..components import Tank, Camera


class Battle(GameScene):

    _map_surface: pygame.Surface = None
    _pressed: Set[int] = None
    _player: IGameObject = None
    _enemy: IGameObject = None

    @property
    def surface(self) -> pygame.Surface:
        return self._map_surface

    def move(self, event_type, key, mods):
        if pygame.KEYDOWN == event_type:
            self._pressed.add(key)
        elif pygame.KEYUP == event_type:
            self._pressed.remove(key)

    def fire(self, *a):
        self._player[Tank].fire()

    def startup(self) -> None:

        #self._map_surface = self.srv_screen.surface.copy()
        self._map_surface = pygame.Surface((4096, 4096))

        self._pressed = set()

        self._camera = self.spawn_object(camera_preset(), self)

        self._player = self.spawn_object(tank_preset(
            name="Player 1",
            controler="NoOp",
            position=(100, 100),
            rotation=0,
            color=(0, 0, 255),
            #props={"bullet_speed":600}
        ), self)

        self._enemy = self.spawn_object(tank_preset(
            name="Player 2",
            controler="NoOp",
            position=(500, 500),
            rotation=0,
            color=(255, 0, 0),
            #props={"bullet_speed":600}
        ), self)

        self.srv_kbd.register_callback(pygame.K_w, self.move, self.move)
        self.srv_kbd.register_callback(pygame.K_a, self.move, self.move)
        self.srv_kbd.register_callback(pygame.K_s, self.move, self.move)
        self.srv_kbd.register_callback(pygame.K_d, self.move, self.move)
        self.srv_kbd.register_callback(pygame.K_RIGHT, self.move, self.move)
        self.srv_kbd.register_callback(pygame.K_LEFT, self.move, self.move)
        self.srv_kbd.register_callback(pygame.K_RETURN, self.fire)
        #self.srv_bus.register_callback(pygame.USEREVENT, print)

        self._camera[Camera].track_object(self._player)

    def shutdown(self) -> None:
        for go in self.all_objects:
            self.kill_object(go)

    def update(self) -> None:
        if pygame.K_w in self._pressed:
            self._player[Tank].move(1)
        if pygame.K_s in self._pressed:
            self._player[Tank].move(-1)
        if pygame.K_a in self._pressed:
            self._player[Tank].turn(-1)
        if pygame.K_d in self._pressed:
            self._player[Tank].turn(1)
        if pygame.K_LEFT in self._pressed:
            self._player[Tank].turn_hat(-1)
        if pygame.K_RIGHT in self._pressed:
            self._player[Tank].turn_hat(1)

