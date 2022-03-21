import pygame
from abc import ABC, abstractmethod
from typing import TypeVar, Type, Optional, Callable, Iterable, List, Dict, Any, Union, Tuple


PROVIDER_T = TypeVar("TYPE_T")
COMPONENT_T = TypeVar("COMPONENT_T", bound="IGameComponent")

KbCallbackDelegate = Callable[[int, int, int], None]
CallbackDelegate = Callable[[pygame.event.Event], None]
FilterDelegate = Callable[[pygame.event.Event], bool]
CollisionDelegate = Callable[["IGameObject"], None]

IDisplayService = pygame.Surface


class IGame(ABC):

    @abstractmethod
    def stop(self): ...


class IServiceBuilder(ABC):

    @abstractmethod
    def get_provider(self, anno: Type[PROVIDER_T]) -> PROVIDER_T: ...

    @abstractmethod
    def get_scene(self, anno: Type["IScene"]) -> "IScene": ...

    @abstractmethod
    def get_component(
        self,
        anno: Union[Type["IGameComponent"], str]
    ) -> "IGameComponent": ...


class IUnifiedMessageServiceInterface(ABC):

    @abstractmethod
    def register_callback(
        self,
        event_type: int,
        callback: CallbackDelegate,
        predicate: FilterDelegate = None
    ) -> None: ...

    @abstractmethod
    def unregister_callback(self, callback: CallbackDelegate) -> None: ...


class IMessageService(IUnifiedMessageServiceInterface):

    @abstractmethod
    def update(self, events: Iterable[pygame.event.Event]): ...


class IKeyboardService:

    def register_callback(
        self,
        key: int,
        keydown_callback: Optional[KbCallbackDelegate] = None,
        keyup_callback: Optional[KbCallbackDelegate] = None,
    ): ...

    def unregister_callback(
        self,
        callback: KbCallbackDelegate
    ) -> None: ...

    def unregister_callbacks(
        self,
        callbacks: Iterable[KbCallbackDelegate]
    ) -> None: ...


class IUnifiedClockServiceInterface(ABC):

    @property
    @abstractmethod
    def frame_delay(self) -> float: ...

    @property
    @abstractmethod
    def frame_delay_ms(self) -> int: ...

    @property
    @abstractmethod
    def frame_rate(self) -> float: ...

    @property
    @abstractmethod
    def now_ms(self) -> int: ...

    @property
    @abstractmethod
    def now(self) -> float: ...


class IClockService(IUnifiedClockServiceInterface):

    @abstractmethod
    def update(self, framerate: int): ...


class IUnifiedObjectServiceInterface(ABC):

    @property
    @abstractmethod
    def all_objects(self) -> List["IGameObject"]: ...

    @abstractmethod
    def add_object(self, go: "IGameObject") -> None: ...

    @abstractmethod
    def remove_object(self, go: "IGameObject") -> None: ...

    @abstractmethod
    def spawn_object(
        self,
        preset: Dict[str, Dict[str, Any]],
        owner: "IUnifiedServiceInterface",
    ) -> "IGameObject": ...

    @abstractmethod
    def kill_object(self, go: "IGameObject") -> None: ...


class IObjectService(IUnifiedObjectServiceInterface):

    @abstractmethod
    def update(self): ...


class IUnifiedSceneServiceInterface(ABC):

    @abstractmethod
    def set_scene(self, scene: Type["IScene"]) -> None: ...

    @abstractmethod
    def push_scene(self, scene: Type["IScene"]) -> None: ...

    @abstractmethod
    def pop_scene(self) -> None: ...

class ISceneService(IUnifiedSceneServiceInterface):

    @abstractmethod
    def update(self): ...


class IUnifiedServiceInterface(
    IUnifiedSceneServiceInterface,
    IUnifiedObjectServiceInterface,
    IUnifiedClockServiceInterface,
    IUnifiedMessageServiceInterface,
): ...


class IGameObject(IUnifiedServiceInterface):

    @property
    @abstractmethod
    def owner(self) -> IUnifiedServiceInterface: ...

    @property
    @abstractmethod
    def alive(self) -> bool: ...

    @property
    @abstractmethod
    def collider(self) -> "ICollider": ...

    @abstractmethod
    def update(self) -> None: ...

    @abstractmethod
    def startup(self) -> None: ...

    @abstractmethod
    def shutdown(self) -> None: ...

    @abstractmethod
    def get(
        self,
        name: Type[COMPONENT_T],
        default: Optional[COMPONENT_T] = None
    ) -> Optional[COMPONENT_T]: ...

    @abstractmethod
    def __setitem__(self, name: Type[COMPONENT_T], value: COMPONENT_T): ...

    @abstractmethod
    def __getitem__(self, name: Type[COMPONENT_T]) -> COMPONENT_T: ...

    @abstractmethod
    def __contains__(self, name: Type[COMPONENT_T]) -> bool: ...

    @abstractmethod
    def __delitem__(self, name: Type[COMPONENT_T]) -> None: ...


class IGameComponent(IUnifiedServiceInterface):

    @property
    @abstractmethod
    def game_object(self) -> "IGameObject": ...

    @game_object.setter
    @abstractmethod
    def game_object(self, g: "IGameObject") -> None: ...

    @abstractmethod
    def startup(self) -> None: ...

    @abstractmethod
    def shutdown(self) -> None: ...

    @abstractmethod
    def update(self) -> None: ...


class ICollider(IGameComponent):

    @abstractmethod
    def check_collision(self, game_object: "IGameObject") -> None: ...

    @abstractmethod
    def collide_rect(self, rect: pygame.Rect) -> bool: ...

    @abstractmethod
    def collide_point(self, point: Tuple[float, float]) -> bool: ...

    @abstractmethod
    def on_collision(self, callback: CollisionDelegate) -> None: ...


class IScene(IUnifiedServiceInterface):

    @property
    @abstractmethod
    def game(self) -> IGame: ...

    @game.setter
    @abstractmethod
    def game(self, game: IGame): ...

    @abstractmethod
    def startup(self) -> None: ...

    @abstractmethod
    def shutdown(self) -> None: ...

    @abstractmethod
    def update_scene(self) -> None: ...

