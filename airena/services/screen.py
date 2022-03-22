import pygame
from ..vector import Vector2
from ..typing import IScreenService


class ScreenService(IScreenService):

    _hw_surface: pygame.Surface

    @property
    def surface(self) -> pygame.Surface:
        return self._hw_surface

    @property
    def screen_flags(self) -> int:
        return self._hw_surface.get_flags()

    def update(self) -> None:
        pygame.display.flip()

    def activate(
        self,
        size: Vector2,
        flags: int = 0,
        display: int = 0,
        vsync: int = 0,
    ) -> None:
        self._hw_surface = pygame.display.set_mode(
            size=size,
            flags=flags,
            display=display,
            vsync=vsync,
        )

