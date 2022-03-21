import pygame
from typing import Set
from ..typing import IGameObject
from ..game_scene import GameScene
from ..presets import tank_preset

from ..components import Tank


class Battle(GameScene):

    pressed: Set[int] = None

    player: IGameObject = None
    enemy: IGameObject = None

    def move(self, event_type, key, mods):
        if pygame.KEYDOWN == event_type:
            self.pressed.add(key)
        elif pygame.KEYUP == event_type:
            self.pressed.remove(key)

    def fire(self, *a):
        self.player[Tank].fire()

    def startup(self) -> None:

        self.pressed = set()

        self.player = self.spawn_object(tank_preset(
            controler="NoOp",
            position=(100, 100),
            rotation=0,
            color=(0, 0, 255),
            #props={"bullet_speed":600}
        ), self)

        self.enemy = self.spawn_object(tank_preset(
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

    def shutdown(self) -> None:
        for go in self.all_objects:
            self.kill_object(go)

    def update(self) -> None:
        if pygame.K_w in self.pressed:
            self.player[Tank].move(1)
        if pygame.K_s in self.pressed:
            self.player[Tank].move(-1)
        if pygame.K_a in self.pressed:
            self.player[Tank].turn(-1)
        if pygame.K_d in self.pressed:
            self.player[Tank].turn(1)
        if pygame.K_LEFT in self.pressed:
            self.player[Tank].turn_hat(-1)
        if pygame.K_RIGHT in self.pressed:
            self.player[Tank].turn_hat(1)
