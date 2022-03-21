import pygame
from argparse import ArgumentParser
from .presets import tank_preset
from .components import Transform, DebugControl, NoOp
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

    def run(self):
        self.obj.spawn(tank_preset(
            controler=DebugControl,
            position=(100, 100),
            rotation=0,
            color=(0, 0, 255),
            #props={"bullet_speed":600}
        ))
        self.obj.spawn(tank_preset(
            controler=NoOp,
            position=(500, 500),
            rotation=0,
            color=(255, 0, 0),
            #props={"bullet_speed":600}
        ))
        self._playing = True
        while self._playing:
            self.bus.update(pygame.event.get())
            self.screen.fill((0, 0, 0))
            self.obj.update()
            pygame.display.flip()
            self.clock.update(60)

    def _toggle_bounding_box(self, *a):
        from .components import BoxCollider
        BoxCollider.show_bounding_box = ~BoxCollider.show_bounding_box

    def __init__(self, ai, bullet_motion_preset: dict):
        builder = ServiceBuilder()
        builder.with_screen((1000, 1000))
        for a in ai:
            builder.using_component(a)
        self.bus = builder.get_provider(IMessageService)
        self.bus.register_callback(pygame.QUIT, lambda x: self.stop())
        self.screen = builder.get_provider(IDisplayService)
        self.clock = builder.get_provider(IClockService)
        self.kbd = builder.get_provider(IKeyboardService)
        self.kbd.register_callback(pygame.K_0, self._toggle_bounding_box)
        self.obj = builder.get_provider(IObjectService)

        spawn_locations = [
            (Vector2(100, 100), 0.75),
            (Vector2(900, 900), -2.25),
            (Vector2(100, 900), -0.75),
            (Vector2(900, 100), 2.25),
        ]

        for (loc, rot), a in zip(spawn_locations, ai):
            self.obj.spawn(tank_preset(
                controler=a,
                position=loc,
                rotation=rot,
                color=a.color,
            ))


if __name__ == "__main__":

    ap = ArgumentParser()
    ap.add_argument("--fire-cooldown", type=float, default=1000)
    ap.add_argument("--bullet-speed", type=float, default=300)
    ap.add_argument("--turn-speed", type=float, default=3)
    ap.add_argument("--move-speed", type=float, default=200)
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
    g = Game(ai,{
        "fire_cooldown": args.fire_cooldown,
        "bullet_speed": args.bullet_speed,
        "turn_speed": args.turn_speed,
        "move_speed": args.move_speed,
    })
    g.run()

