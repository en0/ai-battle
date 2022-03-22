import pygame
from ..game_component import GameComponent
from ..typing import IScreenService, IGameObject
from ..vector import Vector2

from .transform import Transform


class Camera(GameComponent):

    _absolute: pygame.Rect
    _relative: pygame.Rect
    _tracking: IGameObject

    #aperture: Vector2 = Vector2.zero()

    def track_object(self, go: IGameObject) -> None:
        # TODO: Split screen?
        self._tracking = go

    def startup(self):
        self._tracking = self.game_object
        self._relative = self.srv_screen.surface.get_rect()
        self._absolute = self.surface.get_rect()
        self._relative.width = min(self._relative.width, self._absolute.width)
        self._relative.height = min(self._relative.height, self._absolute.height)
        self._tracking[Transform].position = self._relative.center

    def update(self):
        self._relative.center = self._tracking[Transform].position
        self._relative.x = max(self._relative.x, self._absolute.x)
        self._relative.y = max(self._relative.y, self._absolute.y)
        self._relative.right = min(self._relative.right, self._absolute.right)
        self._relative.bottom = min(self._relative.bottom, self._absolute.bottom)
        surface = self.surface.subsurface(self._relative)
        self.srv_screen.surface.blit(surface, (0, 0))

    def __init__(self, srv_screen: IScreenService):
        self.srv_screen = srv_screen
