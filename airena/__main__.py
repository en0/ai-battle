import pygame
from argparse import ArgumentParser
from .presets import tank_preset
from .scenes import Battle
from .builder import ServiceBuilder
from .vector import Vector2
from .typing import (
    IClockService,
    IDisplayService,
    IGame,
    IKeyboardService,
    IMessageService,
    IObjectService,
    ISceneService,
)


class Game(IGame):

    _playing = False

    def stop(self):
        self._playing = False

    def run(self):
        self._playing = True
        self.scn.push_scene(Battle)
        while self._playing:
            self.screen.fill((0, 0, 0))
            self.scn.update()
            pygame.display.flip()
        self.scn.pop_scene()

    def _toggle_bounding_box(self, *a):
        from .components import BoxCollider
        BoxCollider.show_bounding_box = ~BoxCollider.show_bounding_box

    def __init__(self, ai, bullet_motion_preset: dict):
        builder = ServiceBuilder()
        builder.using_constant(self, IGame)
        builder.with_screen((1000, 1000))
        for a in ai:
            builder.using_component(a)
        self.screen = builder.get_provider(IDisplayService)
        self.scn = builder.get_provider(ISceneService)


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

