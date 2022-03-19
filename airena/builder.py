import pygame
import inspect
from pyioc3 import Container, StaticContainerBuilder, ScopeEnum
from typing import TypeVar, Type, Optional, NamedTuple, Union, Callable

from . import components, services
from .lib import Vector2
from .typing import (
    PROVIDER_T,
    IDisplayService,
    IGameComponent,
    IMessageService,
    IKeyboardService,
    IClockService,
    IServiceBuilder,
    IObjectService,
)


ACTIVATE_DELEGATE = Callable[["ServiceBuilder", PROVIDER_T], PROVIDER_T]

class ServiceBuilder(IServiceBuilder):

    _instance: "ServiceBuilder" = None
    _ioc_builder: StaticContainerBuilder = None
    _ioc: Optional[Container] = None

    def get_provider(self, anno: Type[PROVIDER_T]) -> PROVIDER_T:
        self._ensure_built()
        return self._ioc.get(anno)

    def get_component(self, anno: Union[Type[PROVIDER_T], str]) -> PROVIDER_T:
        if inspect.isclass(anno):
            anno = anno.__name__
        return self.get_provider(anno)

    def using_component(
        self,
        component_type: Type[PROVIDER_T]
    ) -> None:
        self.using_provider(component_type, component_type.__name__, scope=ScopeEnum.TRANSIENT)

    def using_provider(
        self,
        impl: Type[PROVIDER_T],
        anno: Optional[Type[PROVIDER_T]] = None,
        scope: ScopeEnum = ScopeEnum.TRANSIENT,
        on_activate: Optional[ACTIVATE_DELEGATE] = None,
    ) -> None:
        self._assert_not_built()
        self._ioc_builder.bind(
            annotation=anno or impl,
            implementation=impl,
            scope=scope,
            on_activate=self._on_activate_wrapper(on_activate)
        )

    def using_constant(
        self,
        val: PROVIDER_T,
        anno: Type[PROVIDER_T],
    ) -> None:
        self._assert_not_built()
        self._ioc_builder.bind_constant(
            annotation=anno,
            value=val,
        )

    def with_screen(self, size: Vector2):

        def setup_screen(*args):
            surface = pygame.display.set_mode(size)
            return surface

        self.using_provider(
            impl=lambda:None,
            anno=IDisplayService,
            scope=ScopeEnum.SINGLETON,
            on_activate=setup_screen
        )

    def _assert_not_built(self):
        if self._ioc is not None:
            raise RuntimeError("Attempt to bind new provider after container in use.")

    def _ensure_built(self):
        if self._ioc is None:
            self._ioc = self._ioc_builder.build()

    def _on_activate_wrapper(self, on_activate):
        def _wrap(inst):
            return on_activate(self, inst)
        return _wrap if on_activate else None

    def _bind_defaults(self):

        # Bind self so it can be injected
        self.using_constant(self, IServiceBuilder)

        # Bind all the built-in components
        for _, obj in inspect.getmembers(components):
            if inspect.isclass(obj) and issubclass(obj, IGameComponent):
                self.using_component(obj)

        self.using_provider(
            services.MessageService,
            IMessageService,
            ScopeEnum.SINGLETON)

        self.using_provider(
            services.KeyboardService,
            IKeyboardService,
            ScopeEnum.SINGLETON)

        self.using_provider(
            services.ClockService,
            IClockService,
            ScopeEnum.SINGLETON)

        self.using_provider(
            services.ObjectService,
            IObjectService,
            ScopeEnum.SINGLETON)

    def __init__(self):
        self._ioc_builder = StaticContainerBuilder()
        self._bind_defaults()

