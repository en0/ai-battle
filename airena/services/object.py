from typing import Dict, Any, Iterable, List, Type, Set
from ..game_object import GameObject
from ..typing import IServiceBuilder, IObjectService, IGameObject, COMPONENT_T
from ..components import Boundary


class ObjectService(IObjectService):

    def spawn(self, tag: str, preset: Dict[str, Dict[str, Any]], owner: IGameObject = None) -> IGameObject:
        comps = [self._load_component(c, a) for c, a in preset.items()]
        go = GameObject(tag, {c.__class__: c for c in comps}, owner)
        go.startup()
        self._alive.append(go)
        self._alive_by_tag.setdefault(tag, []).append(go)
        if Boundary in go and go[Boundary].collidable:
            self._collidable.append(go[Boundary])
        return go

    def kill(self, go: IGameObject) -> None:
        self._to_kill.append(go)

    def update(self):

        if self._to_kill:
            for go in self._to_kill:
                go.shutdown()
                self._alive.remove(go)
                self._alive_by_tag[go.tag].remove(go)
                if Boundary in go and go[Boundary].collidable:
                    self._collidable.remove(go[Boundary])
            self._to_kill.clear()

        for go in self._alive:
            go.update()

        for i in range(len(self._collidable)):
            for j in range(i+1, len(self._collidable)):
                a = self._collidable[i]
                b = self._collidable[j]
                a.check_collision(b.game_object)
                b.check_collision(a.game_object)

    def get_objects_containing_components(
        self,
        component_t: Type[COMPONENT_T]
    ) -> Iterable[IGameObject]:
        for go in self._alive:
            if component_t in go:
                yield go

    def get_objects_by_tag(self, tag) -> List[IGameObject]:
        return self._alive_by_tag.get(tag, [])

    def _load_component(self, comp_t, args):
        comp = self._loc.get_component(comp_t)
        for name, val in (args or {}).items():
            setattr(comp, name, val)
        return comp

    def __init__(self, builder: IServiceBuilder):
        self._loc = builder
        self._alive: List[IGameObject] = []
        self._to_kill: List[IGameObject] = []
        self._collidable: List[Boundary] = []
        self._alive_by_tag: Dict[str, IGameObject] = {}
