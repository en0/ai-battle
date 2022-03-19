import pygame
from argparse import ArgumentParser
from .components import Transform
from .builder import ServiceBuilder
from .vector import Vector2
from .typing import (
    IMessageService,
    IClockService,
    IDisplayService,
    IKeyboardService,
    IObjectService,
)


class Game:

    _playing = False

    def stop(self):
        self._playing = False

    def kill_player(self):
        if self.player:
            self.obj.kill(self.player)
            self.player = None

    def run(self):
        self._playing = True
        while self._playing:
            self.bus.update(pygame.event.get())
            self.screen.fill((0, 0, 0))
            self.obj.update()
            pygame.display.flip()
            self.clock.update(60)

    def __init__(self, ai):
        builder = ServiceBuilder()
        builder.with_screen((500, 500))
        for a in ai:
            builder.using_component(a)
        self.bus = builder.get_provider(IMessageService)
        self.bus.register_callback(pygame.QUIT, lambda x: self.stop())
        self.screen = builder.get_provider(IDisplayService)
        self.clock = builder.get_provider(IClockService)
        self.kb = builder.get_provider(IKeyboardService)
        self.kb.register_callback(pygame.K_0, lambda *_: self.kill_player())
        self.obj = builder.get_provider(IObjectService)

        spawn_locations = [
            Vector2(150, 150),
            Vector2(350, 150),
            Vector2(150, 350),
            Vector2(350, 350),
        ]

        for loc, a in zip(spawn_locations, ai):
            self.obj.spawn("Tank", {
                a.__name__: None,
                "TankRenderer": {"color": a.color},
                "BotMotion": None,
                "Transform": {"position": loc},
                "Boundary": {"height": 10, "width": 10, "collidable": True}
            })


if __name__ == "__main__":

    ap = ArgumentParser()
    ap.add_argument("bot", nargs="*")
    args = ap.parse_args()

    import inspect
    import importlib
    from airena.components.ai_base import AiBase
    from os.path import basename

    ai = []
    for p in args.bot:
        spec = importlib.util.spec_from_file_location(basename(p)[:-3], p)
        mod = importlib.util.module_from_spec(spec)
        mod = importlib.import_module(basename(p)[:-3], mod)
        for name, mem in inspect.getmembers(mod):
            if inspect.isclass(mem) and mem is not AiBase and issubclass(mem, AiBase):
                ai.append(mem)

    pygame.init()
    g = Game(ai)
    g.run()

