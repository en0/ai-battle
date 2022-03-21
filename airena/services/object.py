from typing import Dict, Any, Iterable, List, Type, Set
from ..game_object import GameObject
from ..typing import IServiceBuilder, IObjectService, IGameObject, COMPONENT_T, ICollider


class ObjectService(IObjectService):

    def spawn(self, preset: Dict[str, Dict[str, Any]], owner: IGameObject = None) -> IGameObject:
        comps = [self._load_component(c, a) for c, a in preset.items()]
        go = GameObject({c.__class__: c for c in comps}, owner)
        go.startup()
        self._alive.append(go)
        if go.collider:
            self._collidable.append(go.collider)
        return go

    def kill(self, go: IGameObject) -> None:
        self._to_kill.append(go)

    def update(self):
        self._do_kills()
        self._do_updates()
        self._do_collisions()

    def get_objects_by_tag(self, tag) -> List[IGameObject]:
        return self._alive_by_tag.get(tag, [])

    def _do_kills(self):
        for go in self._to_kill:
            go.shutdown()
            self._alive.remove(go)
            #self._alive_by_tag[go.tag].remove(go)
            if go.collider:
                self._collidable.remove(go.collider)
        if self._to_kill:
            self._to_kill.clear()

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

    def _load_component(self, comp_t, args):
        comp = self._loc.get_component(comp_t)
        for name, val in (args or {}).items():
            setattr(comp, name, val)
        return comp

    def __init__(self, builder: IServiceBuilder):
        self._loc = builder
        self._alive: List[IGameObject] = []
        self._to_kill: List[IGameObject] = []
        self._collidable: List[ICollider] = []
        self._alive_by_tag: Dict[str, IGameObject] = {}
