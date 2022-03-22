import pygame
from abc import abstractmethod
from typing import Type, List, Dict, Any
from .vector import Vector2
from .typing import IGameComponent, IGameObject, IScene, CallbackDelegate, FilterDelegate


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

    # IUnifiedScreenServiceInterface

    @property
    def surface(self) -> pygame.Surface:
        return self._owner.surface

    @property
    def screen_flags(self) -> int:
        return self._owner.screen_flags

    # IUnifiedSceneServiceInterface

    def set_scene(self, scene: Type[IScene]) -> None:
        self._owner.set_scene(scene)

    def push_scene(self, scene: Type[IScene]) -> None:
        self._owner.push_scene(scene)

    def pop_scene(self) -> None:
        self._owner.pop_scene()

    # IUnifiedObjectServiceInterface

    @property
    def all_objects(self) -> List[IGameObject]:
        return self._owner.all_objects()

    def add_object(self, go: IGameObject) -> None:
        self._owner.add_object(go)

    def remove_object(self, go: IGameObject) -> None:
        self._owner.remove_object(go)

    def spawn_object(
        self,
        preset: Dict[str, Dict[str, Any]],
        owner: IGameObject
    ) -> IGameObject:
        return self._owner.spawn_object(preset, owner)

    def kill_object(self, go: IGameObject) -> None:
        self._owner.kill_object(go)

    # IUnifiedClockServiceInterface

    @property
    def frame_delay(self) -> float:
        return self._owner.frame_delay

    @property
    def frame_delay_ms(self) -> int:
        return self._owner.frame_delay_ms

    @property
    def frame_rate(self) -> float:
        return self._owner.frame_rate

    @property
    def now_ms(self) -> int:
        return self._owner.now_ms

    @property
    def now(self) -> float:
        return self._owner.now

    # IUnifiedMessageServiceInterface

    def register_callback(
        self,
        event_type: int,
        callback: CallbackDelegate,
        predicate: FilterDelegate = None
    ) -> None:
        self._owner.register_callback(event_type, callback, predicate)

    def unregister_callback(self, callback: CallbackDelegate) -> None:
        self._owner.unregister_callback(callback)

    def broadcast(self, name: str, **data):
        self._owner.broadcast(name, **data)

