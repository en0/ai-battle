from unittest import TestCase, skip
from unittest.mock import Mock
from airena.game_object import GameObject
from airena.typing import IGameComponent
from tests.mocks.component_mock import ComponentMock


class GameObjectTest(TestCase):

    def setUp(self):
        self.go = GameObject()
        self.component1 = ComponentMock()
        self.component2 = ComponentMock()

    def test_can_set_component(self):
        self.go = GameObject()
        self.go[ComponentMock] = self.component1
        self.assertIn(ComponentMock, self.go)

    def test_added_component_sets_owner(self):
        self.go = GameObject()
        self.go[ComponentMock] = self.component1
        self.assertIs(self.component1.game_object, self.go)

    def test_remove_component(self):
        self.go = GameObject()
        self.go[ComponentMock] = self.component1
        del self.go[ComponentMock]
        self.assertNotIn(ComponentMock, self.go)

    def test_remove_component_unset_owner(self):
        self.go = GameObject()
        self.go[ComponentMock] = self.component1
        del self.go[ComponentMock]
        self.assertIsNone(self.component1.game_object)

    def test_removed_component_has_owner_unset(self):
        self.go = GameObject()
        self.go[ComponentMock] = self.component1
        self.assertIs(self.component1.game_object, self.go)
        self.go[ComponentMock] = self.component2
        self.assertIsNone(self.component1.game_object)

    def test_can_get_component(self):
        self.go = GameObject()
        self.go[ComponentMock] = self.component1
        self.assertIs(self.go[ComponentMock], self.component1)

    def test_can_get_component_through_get(self):
        self.go = GameObject()
        self.go[ComponentMock] = self.component1
        self.assertIs(self.go.get(ComponentMock), self.component1)

    def test_can_get_component_default(self):
        sentinal = object()
        self.assertIs(self.go.get(ComponentMock, sentinal), sentinal)

    def test_update_calls_update_on_all_components(self):
        self.go[ComponentMock] = self.component1
        self.component1.update = Mock()
        self.go.update()
        self.component1.update.assert_called()

