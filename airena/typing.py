import pygame
from abc import ABC, abstractmethod
from typing import TypeVar, Type, Optional, Callable, Iterable, List, Dict, Any, Union


PROVIDER_T = TypeVar("TYPE_T")

KbCallbackDelegate = Callable[[int, int, int], None]
CallbackDelegate = Callable[[pygame.event.Event], None]
FilterDelegate = Callable[[pygame.event.Event], bool]

IDisplayService = pygame.Surface


class IGameComponent(ABC):

    @property
    @abstractmethod
    def game_object(self) -> "IGameObject":
        ...

    @game_object.setter
    @abstractmethod
    def game_object(self, g: "IGameObject") -> None:
        ...

    @abstractmethod
    def startup(self) -> None:
        ...

    @abstractmethod
    def shutdown(self) -> None:
        ...

    @abstractmethod
    def update(self) -> None:
        ...


COMPONENT_T = TypeVar("COMPONENT_T", bound=IGameComponent)


class IGameObject(ABC):

    @property
    @abstractmethod
    def owner(self) -> Optional["IGameObject"]:
        ...

    @property
    @abstractmethod
    def tag(self) -> str:
        ...

    @abstractmethod
    def update(self) -> None:
        ...

    @abstractmethod
    def startup(self) -> None:
        ...

    @abstractmethod
    def shutdown(self) -> None:
        ...

    @abstractmethod
    def get(self, name: Type[COMPONENT_T], default: Optional[COMPONENT_T] = None) -> Optional[COMPONENT_T]:
        ...

    @abstractmethod
    def __setitem__(self, name: Type[COMPONENT_T], value: COMPONENT_T):
        ...

    @abstractmethod
    def __getitem__(self, name: Type[COMPONENT_T]) -> COMPONENT_T:
        ...

    @abstractmethod
    def __contains__(self, name: Type[COMPONENT_T]) -> bool:
        ...

    @abstractmethod
    def __delitem__(self, name: Type[COMPONENT_T]) -> None:
        ...


class IMessageService(ABC):

    @abstractmethod
    def register_callback(
        self,
        event_type: int,
        callback: CallbackDelegate,
        predicate: FilterDelegate = None
    ):
        ...

    @abstractmethod
    def unregister_callback(self, callback: CallbackDelegate):
        ...

    @abstractmethod
    def update(self, events: Iterable[pygame.event.Event]):
        ...


class IKeyboardService:
    def register_callback(
        self,
        key: int,
        keydown_callback: Optional[KbCallbackDelegate] = None,
        keyup_callback: Optional[KbCallbackDelegate] = None,
    ):
        ...

    def unregister_callback(self, callback: KbCallbackDelegate) -> None:
        ...

    def unregister_callbacks(self, callbacks: Iterable[KbCallbackDelegate]) -> None:
        ...


class IClockService(ABC):
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

    @abstractmethod
    def update(self, framerate: int): ...


class IServiceBuilder(ABC):

    @abstractmethod
    def get_provider(self, anno: Type[PROVIDER_T]) -> PROVIDER_T:
        ...

    @abstractmethod
    def get_component(self, anno: Union[Type[PROVIDER_T], str]) -> PROVIDER_T:
        ...

class IObjectService(ABC):

    @abstractmethod
    def get_objects_by_tag(self, tag) -> List[IGameObject]:
        ...

    @abstractmethod
    def spawn(self, tag: str, preset: Dict[str, Dict[str, Any]], owner: IGameObject = None) -> IGameObject:
        ...

    @abstractmethod
    def kill(self, go: IGameObject) -> None:
        ...

    @abstractmethod
    def update(self) -> None:
        ...
