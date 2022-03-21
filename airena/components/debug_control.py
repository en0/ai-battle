import pygame

from ..typing import IKeyboardService
from ..game_component import GameComponent
from ..vector import Vector2

from .transform import Transform
from .tank import Tank


class DebugControl(GameComponent):

    def move(self, event_type, key, mods):
        if pygame.KEYDOWN == event_type:
            self._pressed.add(key)
        elif pygame.KEYUP == event_type:
            self._pressed.remove(key)

    def fire(self, *a):
        self.ctrl.fire()

    def startup(self) -> None:
        self.kb.register_callback(pygame.K_w, self.move, self.move)
        self.kb.register_callback(pygame.K_a, self.move, self.move)
        self.kb.register_callback(pygame.K_s, self.move, self.move)
        self.kb.register_callback(pygame.K_d, self.move, self.move)
        self.kb.register_callback(pygame.K_RIGHT, self.move, self.move)
        self.kb.register_callback(pygame.K_LEFT, self.move, self.move)
        self.kb.register_callback(pygame.K_RETURN, self.fire)
        self.ctrl = self.game_object[Tank]

    def shutdown(self) -> None:
        self.kb.unregister_callbacks([self.move, self.fire])

    def update(self) -> None:
        if pygame.K_w in self._pressed:
            self.ctrl.move(1)
        if pygame.K_s in self._pressed:
            self.ctrl.move(-1)
        if pygame.K_a in self._pressed:
            self.ctrl.turn(-1)
        if pygame.K_d in self._pressed:
            self.ctrl.turn(1)
        if pygame.K_LEFT in self._pressed:
            self.ctrl.turn_hat(-1)
        if pygame.K_RIGHT in self._pressed:
            self.ctrl.turn_hat(1)

    def __init__(self, kb: IKeyboardService):
        self.kb = kb
        self._pressed = set()
