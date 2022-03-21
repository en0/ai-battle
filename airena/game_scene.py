import pygame
from abc import abstractmethod
from typing import Type, List, Dict, Any
from .typing import (
    CallbackDelegate,
    FilterDelegate,
    IClockService,
    IGame,
    IGameObject,
    IKeyboardService,
    IMessageService,
    IObjectService,
    IScene,
    ISceneService,
    IUnifiedServiceInterface,
)


class GameScene(IScene):

    @property
    def game(self) -> IGame:
        return self._game

    @game.setter
    def game(self, game: IGame):
        self._game = game

    @abstractmethod
    def update(self) -> None:
        ...

    def startup(self) -> None:
        ...

    def shutdown(self) -> None:
        ...

    def update_scene(self) -> None:
        self.srv_bus.update(pygame.event.get())
        self.update()
        self.srv_object.update()
        self.srv_clock.update(60)

    # IUnifiedSceneServiceInterface

    def set_scene(self, scene: Type[IScene]) -> None:
        self.srv_scene.set_scene(scene)

    def push_scene(self, scene: Type[IScene]) -> None:
        self.srv_scene.push_scene(scene)

    def pop_scene(self) -> None:
        self.srv_scene.pop_scene()

    # IUnifiedObjectServiceInterface

    @property
    def all_objects(self) -> List[IGameObject]:
        return self.srv_object.all_objects

    def add_object(self, go: IGameObject) -> None:
        self.srv_object.add_object(go)

    def remove_object(self, go: IGameObject) -> None:
        self.srv_object.remove_object(go)

    def spawn_object(
        self,
        preset: Dict[str, Dict[str, Any]],
        owner: IUnifiedServiceInterface,
    ) -> IGameObject:
        return self.srv_object.spawn_object(preset, owner)

    def kill_object(self, go: IGameObject) -> None:
        self.srv_object.kill_object(go)

    # IUnifiedClockServiceInterface

    @property
    def frame_delay(self) -> float:
        return self.srv_clock.frame_delay

    @property
    def frame_delay_ms(self) -> int:
        return self.srv_clock.frame_delay_ms

    @property
    def frame_rate(self) -> float:
        return self.srv_clock.frame_rate

    @property
    def now_ms(self) -> int:
        return self.srv_clock.now_ms

    @property
    def now(self) -> float:
        return self.srv_clock.now

    # IUnifiedMessageServiceInterface

    def register_callback(
        self,
        event_type: int,
        callback: CallbackDelegate,
        predicate: FilterDelegate = None
    ) -> None:
        self.srv_bus.register_callback(event_type, callback, predicate)

    def unregister_callback(self, callback: CallbackDelegate) -> None:
        self.srv_bus.unregister_callback(callback)

    def __init__(
        self,
        game: IGame,
        srv_scene: ISceneService,
        srv_object: IObjectService,
        srv_clock: IClockService,
        srv_bus: IMessageService,
        srv_kbd: IKeyboardService,
    ) -> None:
        self._game = game
        self.srv_scene = srv_scene
        self.srv_object = srv_object
        self.srv_clock = srv_clock
        self.srv_bus = srv_bus
        self.srv_kbd = srv_kbd
        self.srv_bus.register_callback(
            pygame.QUIT,
            lambda *a: game.stop()
        )
