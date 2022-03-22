import pygame
from typing import Type, Optional, Dict, List, Any
from .vector import Vector2
from .typing import (
    COMPONENT_T,
    CallbackDelegate,
    FilterDelegate,
    ICollider,
    IGameComponent,
    IGameObject,
    IUnifiedServiceInterface,
    IScene,
)


class GameObject(IGameObject):

    @property
    def owner(self) -> IUnifiedServiceInterface:
        return self._owner

    @property
    def alive(self) -> bool:
        return self._alive

    @property
    def collider(self) -> ICollider:
        return self._collider

    def update(self) -> None:
        for component in self._components.values():
            component.update()

    def startup(self) -> None:
        self._alive = True
        for component in self._components.values():
            component.startup()

    def shutdown(self) -> None:
        self._alive = False
        for component in self._components.values():
            component.shutdown()

    def get(self, name: Type[COMPONENT_T], default: Optional[COMPONENT_T] = None) -> Optional[COMPONENT_T]:
        if name not in self:
            return default
        return self[name]

    def __setitem__(self, name: Type[COMPONENT_T], value: COMPONENT_T):
        if name in self:
            del self[name]
        self._components[name] = value
        if issubclass(name, ICollider):
            self._collider = value
        value.game_object = self

    def __getitem__(self, name: Type[COMPONENT_T]) -> COMPONENT_T:
        return self._components[name]

    def __contains__(self, name: Type[COMPONENT_T]) -> bool:
        return name in self._components

    def __delitem__(self, name: Type[COMPONENT_T]) -> None:
        val = self._components[name]
        val.game_object = None
        del self._components[name]
        if val is self._collider:
            self._collider = None

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

    def __init__(
        self,
        owner: IUnifiedServiceInterface,
        components: Dict[Type[COMPONENT_T], COMPONENT_T] = None
    ) -> None:
        self._alive = False
        self._owner = owner
        self._components: Dict[Type[COMPONENT_T], COMPONENT_T] = {}
        self._collider: ICollider = None
        for anno, comp in (components or {}).items():
            self[anno] = comp

