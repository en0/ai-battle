from typing import Type, Optional, Dict
from .typing import (
    COMPONENT_T,
    IGameObject,
    IGameComponent,
)


class GameObject(IGameObject):

    @property
    def owner(self) -> Optional[IGameObject]:
        return self._owner

    @property
    def alive(self) -> bool:
        return self._alive

    @property
    def tag(self) -> str:
        return self._tag

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
        value.game_object = self

    def __getitem__(self, name: Type[COMPONENT_T]) -> COMPONENT_T:
        return self._components[name]

    def __contains__(self, name: Type[COMPONENT_T]) -> bool:
        return name in self._components

    def __delitem__(self, name: Type[COMPONENT_T]) -> None:
        self._components[name].game_object = None
        del self._components[name]

    def __init__(self, tag: str, components: Dict[Type[COMPONENT_T], COMPONENT_T] = None, owner: IGameObject = None):
        self._tag = tag
        self._owner = owner
        self._alive = False
        self._components: Dict[Type[COMPONENT_T], COMPONENT_T] = {}
        for anno, comp in (components or {}).items():
            self[anno] = comp

