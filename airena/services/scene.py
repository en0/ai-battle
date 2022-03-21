from typing import Deque, Type
from collections import deque
from ..typing import IScene, ISceneService, IServiceBuilder


class SceneService(ISceneService):

    def set_scene(self, scene: Type[IScene]):
        self.pop_scene()
        self.push_scene(scene)

    def push_scene(self, scene: Type[IScene]):
        _scene = self._builder.get_scene(scene)
        _scene.startup()
        self._stack.append(_scene)

    def pop_scene(self):
        scene = self._stack.pop()
        scene.shutdown()

    def update(self):
        # TODO: We cannot allow scene change out of band!
        # Update this function to do scene changes after updates are complete
        if self._stack:
            self._stack[-1].update_scene()

    def __init__(self, builder: IServiceBuilder) -> None:
        self._stack: Deque[IScene] = deque()
        self._builder = builder
