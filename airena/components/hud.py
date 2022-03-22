import pygame
from ..typing import IScreenService
from ..game_component import GameComponent
from ..components import Meta


class HeadsUpDisplay(GameComponent):

    _health = None
    _font: pygame.font.Font = None

    def _receive_update(self, event) -> None:
        name = event.owner[Meta]["name"]
        self._health[name] = event.value

    def _remove_tank(self, event) -> None:
        name = event.owner[Meta]["name"]
        del self._health[name]

    def startup(self):
        font_name = pygame.font.get_default_font()
        self._font = pygame.font.SysFont(font_name, 72)
        self._health = {}
        self.register_callback(
            pygame.USEREVENT,
            self._receive_update,
            lambda e: e.name == "Meta:health")
        self.register_callback(
            pygame.USEREVENT,
            self._remove_tank,
            lambda e: e.name == "Tank:killed")

    def update(self):
        for i, (k, v) in enumerate(self._health.items()):
            text = self._font.render(f"{k}: {v}", True, (0, 0, 255))
            self.srv_screen.surface.blit(text, (0, i*50))

    def __init__(self, srv_screen: IScreenService) -> None:
        self.srv_screen = srv_screen

