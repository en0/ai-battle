import pygame
from itertools import tee
from unittest import TestCase
from unittest.mock import Mock

from airena.services.message import MessageService


class MessageServiceTest(TestCase):

    def setUp(self):
        self.unit = MessageService()

    def mock_event(self, event_type, **kwargs):
        return pygame.event.Event(event_type, **kwargs)

    def mock_events(self, event_types, **kwargs):
        for event_type in event_types:
            yield self.mock_event(event_type, **kwargs)

    def reset_mocks(self, mocks):
        for mock in mocks:
            mock.reset_mock()

    def test_message_bus(self):

        cb1, cb2 = Mock(), Mock()
        self.unit.register_callback(100, cb1)
        self.unit.register_callback(100, cb2)

        cb3 = Mock()
        self.unit.register_callback(100, cb3)
        self.unit.register_callback(101, cb3)
        self.unit.register_callback(102, cb3)

        cb4 = Mock()
        self.unit.register_callback(103, cb4)

        cb5 = Mock()
        self.unit.register_callback(100, cb5)
        self.unit.register_callback(101, cb5)
        self.unit.register_callback(102, cb5)
        self.unit.register_callback(103, cb5)
        self.unit.register_callback(104, cb5)

        events = list(self.mock_events([100, 101, 102, 103, 104]))
        e100, e101, e102, e103, e104 = events

        self.unit.update(iter(events))
        cb1.assert_called_once_with(e100)
        cb2.assert_called_once_with(e100)
        cb3.assert_any_call(e100)
        cb3.assert_any_call(e101)
        cb3.assert_any_call(e102)
        cb4.assert_called_once_with(e103)
        cb5.assert_any_call(e100)
        cb5.assert_any_call(e101)
        cb5.assert_any_call(e102)
        cb5.assert_any_call(e103)
        cb5.assert_any_call(e104)

        self.unit.unregister_callback(cb5)
        self.reset_mocks([cb1,cb2,cb3,cb4,cb5])

        self.unit.update(events)
        cb1.assert_called_once_with(e100)
        cb2.assert_called_once_with(e100)
        cb3.assert_any_call(e100)
        cb3.assert_any_call(e101)
        cb3.assert_any_call(e102)
        cb4.assert_called_once_with(e103)
        cb5.assert_not_called()

        self.unit.unregister_callback(cb4)
        self.reset_mocks([cb1,cb2,cb3,cb4,cb5])

        self.unit.update(events)
        cb1.assert_called_once_with(e100)
        cb2.assert_called_once_with(e100)
        cb3.assert_any_call(e100)
        cb3.assert_any_call(e101)
        cb3.assert_any_call(e102)
        cb4.assert_not_called()
        cb5.assert_not_called()

        self.unit.unregister_callback(cb3)
        self.reset_mocks([cb1,cb2,cb3,cb4,cb5])

        self.unit.update(events)
        cb1.assert_called_once_with(e100)
        cb2.assert_called_once_with(e100)
        cb3.assert_not_called()
        cb4.assert_not_called()
        cb5.assert_not_called()

        self.unit.unregister_callback(cb2)
        self.reset_mocks([cb1,cb2,cb3,cb4,cb5])

        self.unit.update(events)
        cb1.assert_called_once_with(e100)
        cb2.assert_not_called()
        cb3.assert_not_called()
        cb4.assert_not_called()
        cb5.assert_not_called()

        self.unit.unregister_callback(cb1)
        self.reset_mocks([cb1,cb2,cb3,cb4,cb5])

        self.unit.update(events)
        cb1.assert_not_called()
        cb2.assert_not_called()
        cb3.assert_not_called()
        cb4.assert_not_called()
        cb5.assert_not_called()
