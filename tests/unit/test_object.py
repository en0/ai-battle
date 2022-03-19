from unittest import TestCase
from unittest.mock import Mock
from airena.builder import ServiceBuilder
from airena.typing import IObjectService, IDisplayService
from airena.lib import Vector2

from airena import components


class ObjectServiceTests(TestCase):

    def setUp(self):
        self.builder = ServiceBuilder()
        self.builder.using_provider(Mock(), IDisplayService)
        self.unit = self.builder.get_provider(IObjectService)

    def test_spawn_creates_game_object(self):
        go = self.unit.spawn("x", {
            "TankRenderer": {"radius": 50},
            "BotMotion": {"collidable": True},
            "Transform": {"position": Vector2(250, 250)},
        })
        self.assertIn(components.TankRenderer, go)
        self.assertIn(components.BotMotion, go)
        self.assertIn(components.Transform, go)

    def test_spawn_initilizes_circle_renderer(self):
        go = self.unit.spawn("x", {
            "TankRenderer": {"radius": 50},
            "BotMotion": {"collidable": True},
            "Transform": {"position": Vector2(250, 250)},
        })
        comp = go[components.TankRenderer]
        self.assertIsInstance(comp, components.TankRenderer)
        self.assertEqual(comp.radius, 50)

    def test_spawn_initilizes_bot_motion(self):
        go = self.unit.spawn("x", {
            "TankRenderer": {"radius": 50},
            "BotMotion": {"collidable": True},
            "Transform": {"position": Vector2(250, 250)},
        })
        comp = go[components.BotMotion]
        self.assertIsInstance(comp, components.BotMotion)
        self.assertEqual(comp.collidable, True)

    def test_spawn_initilizes_transform(self):
        go = self.unit.spawn("x", {
            "TankRenderer": {"radius": 50},
            "BotMotion": {"collidable": True},
            "Transform": {"position": Vector2(250, 250)},
        })
        comp = go[components.Transform]
        self.assertIsInstance(comp, components.Transform)
        self.assertEqual(comp.position, Vector2(250, 250))
