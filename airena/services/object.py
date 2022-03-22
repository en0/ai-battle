from typing import Dict, Any, Iterable, List, Type, Set, Deque
from collections import deque
from ..game_object import GameObject
from ..typing import (
    COMPONENT_T,
    ICollider,
    IGameObject,
    IObjectService,
    IServiceBuilder,
)


class ObjectService(IObjectService):

    @property
    def all_objects(self) -> List[IGameObject]:
        return self._alive.copy()

    def spawn_object(self, preset: Dict[str, Dict[str, Any]], owner: IGameObject = None) -> IGameObject:
        comps = [self._load_component(c, a) for c, a in preset.items()]
        go = GameObject(owner, {c.__class__: c for c in comps})
        go.startup()
        self.add_object(go)
        return go

    def kill_object(self, go: IGameObject) -> None:
        self._to_kill.appendleft(go)

    def add_object(self, go: IGameObject) -> None:
        self._to_add.appendleft(go)

    def remove_object(self, go: IGameObject) -> None:
        self._to_remove.appendleft(go)

    def update(self):
        self._do_adds()
        self._do_updates()
        self._do_collisions()
        self._do_kills()
        self._do_removes()


    def _do_adds(self):
        while self._to_add:
            go = self._to_add.pop()
            self._add_object(go)

    def _do_updates(self):
        for go in self._alive:
            go.update()

    def _do_collisions(self):
        for i in range(len(self._collidable)):
            for j in range(i+1, len(self._collidable)):
                a = self._collidable[i]
                b = self._collidable[j]
                a.check_collision(b.game_object)
                b.check_collision(a.game_object)

    def _do_kills(self):
        while self._to_kill:
            go = self._to_kill.pop()
            go.shutdown()
            self._remove_object(go)

    def _do_removes(self):
        while self._to_remove:
            go = self._to_remove.pop()
            self._remove_object(go)

    def _add_object(self, go):
        self._alive.appendleft(go)
        if go.collider:
            self._collidable.appendleft(go.collider)

    def _remove_object(self, go):
        self._alive.remove(go)
        if go.collider:
            self._collidable.remove(go.collider)

    def _load_component(self, comp_t, args):
        comp = self.srv_builder.get_component(comp_t)
        for name, val in (args or {}).items():
            setattr(comp, name, val)
        return comp

    def __init__(self, builder: IServiceBuilder):
        self.srv_builder = builder

        self._to_add: Deque[IGameObject] = deque()
        self._to_kill: Deque[IGameObject] = deque()
        self._to_remove: Deque[IGameObject] = deque()

        self._alive: Deque[IGameObject] = deque()
        self._collidable: Deque[ICollider] = deque()
        self._alive_by_tag: Dict[str, IGameObject] = {}
