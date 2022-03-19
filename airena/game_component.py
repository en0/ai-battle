from abc import abstractmethod
from .typing import IGameComponent, IGameObject


class GameComponent(IGameComponent):

    _owner: IGameObject = None

    @property
    def game_object(self) -> IGameObject:
        return self._owner

    @game_object.setter
    def game_object(self, g: IGameObject) -> None:
        self._owner = g

    def startup(self) -> None:
        ...

    def shutdown(self) -> None:
        ...

    def update(self) -> None:
        ...

