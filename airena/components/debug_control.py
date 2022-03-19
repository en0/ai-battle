import pygame

from ..typing import IKeyboardService
from ..game_component import GameComponent
from ..lib import Vector2

from .transform import Transform
from .bot_motion import BotMotion


class DebugControl(GameComponent):

    def k1(self, *a):
        self.rb.set_focus(Vector2(350, 350))
        self.rb.move_toword(Vector2(350, 350))

    def k2(self, *a):
        self.rb.set_focus(Vector2(150, 350))
        self.rb.move_toword(Vector2(150, 350))

    def k3(self, *a):
        self.rb.set_focus(Vector2(350, 150))
        self.rb.move_toword(Vector2(350, 150))

    def k4(self, *a):
        self.rb.set_focus(Vector2(250, 250))
        self.rb.move_toword(Vector2(250, 250))

    def kenter(self, *a):
        self.rb.fire()

    def w(self, *a):
        self.rb.move_forward()

    def a(self, *a):
        self.rb.move_left()

    def s(self, *a):
        self.rb.move_backward()

    def d(self, *a):
        self.rb.move_right()

    def startup(self) -> None:
        self.kb.register_callback(pygame.K_1, self.k1)
        self.kb.register_callback(pygame.K_2, self.k2)
        self.kb.register_callback(pygame.K_3, self.k3)
        self.kb.register_callback(pygame.K_4, self.k4)
        self.kb.register_callback(pygame.K_RETURN, self.kenter)
        self.kb.register_callback(pygame.K_w, self.w)
        self.kb.register_callback(pygame.K_a, self.a)
        self.kb.register_callback(pygame.K_s, self.s)
        self.kb.register_callback(pygame.K_d, self.d)
        self.rb = self.game_object[BotMotion]

    def shutdown(self) -> None:
        self.kb.unregister_callbacks([
            self.k1, self.k2,
            self.k3, self.k4,
            self.w, self.a,
            self.s, self.d,
            self.kenter
        ])

    def update(self) -> None:
        ...

    def __init__(self, kb: IKeyboardService):
        self.kb = kb
