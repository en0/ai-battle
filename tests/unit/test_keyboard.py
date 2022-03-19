import pygame
from unittest import TestCase
from unittest.mock import Mock
from airena.services import KeyboardService, MessageService

D = pygame.KEYDOWN
U = pygame.KEYUP

K1 = pygame.K_1
K2 = pygame.K_2
K3 = pygame.K_3
K4 = pygame.K_4

K1D = (D, K1)
K2D = (D, K2)
K3D = (D, K3)
K4D = (D, K4)

K1U = (U, K1)
K2U = (U, K2)
K3U = (U, K3)
K4U = (U, K4)

class KeyboardServiceTests(TestCase):

    def setUp(self):
        self.bus = MessageService()
        self.unit = KeyboardService(self.bus)

        cb1_down, cb1_up = Mock(), Mock()
        self.unit.register_callback(K1, cb1_down, cb1_up)

        cb2 = Mock()
        self.unit.register_callback(K2, cb2, cb2)

        cb3_up = Mock()
        self.unit.register_callback(K3, keyup_callback=cb3_up)

        cb4_1, cb4_2 = Mock(), Mock()
        self.unit.register_callback(K4, cb4_1)
        self.unit.register_callback(K4, cb4_2)

        cb1_again_down, cb1_again_up = Mock(), Mock()
        self.unit.register_callback(K1, cb1_again_down, cb1_again_up)

        self.cb1_down = cb1_down
        self.cb1_up = cb1_up
        self.cb2 = cb2
        self.cb3_up = cb3_up
        self.cb4_1 = cb4_1
        self.cb4_2 = cb4_2
        self.cb1_again_down = cb1_again_down
        self.cb1_again_up = cb1_again_up

    def send_keys(self, strokes, mod=0):
        events = [pygame.event.Event(t, key=k, mod=mod) for t, k in strokes]
        self.bus.update(events)
        return events

    def test_all_keys(self):
        self.send_keys([K1D, K2D, K3D, K4D, K1U, K2U, K3U, K4U])
        self.cb1_down.assert_called_once_with(D, K1, 0)
        self.cb1_up.assert_called_once_with(U, K1, 0)
        self.cb2.assert_any_call(D, K2, 0)
        self.cb2.assert_any_call(U, K2, 0)
        self.cb3_up.assert_called_once_with(U, K3, 0)
        self.cb4_1.assert_called_once_with(D, K4, 0)
        self.cb4_2.assert_called_once_with(D, K4, 0)
        self.cb1_again_down.assert_called_once_with(D, K1, 0)
        self.cb1_again_up.assert_called_once_with(U, K1, 0)

    def test_called_twice(self):
        self.send_keys([K1D, K1U, K1D, K1U])
        self.assertEqual(self.cb1_down.call_count, 2)
        self.assertEqual(self.cb1_up.call_count, 2)

    def test_unregister_cb_again(self):
        self.unit.unregister_callbacks([self.cb1_again_down, self.cb1_again_up])
        self.send_keys([K1D, K2D, K3D, K4D, K1U, K2U, K3U, K4U])
        self.cb1_down.assert_called_once_with(D, K1, 0)
        self.cb1_up.assert_called_once_with(U, K1, 0)
        self.cb2.assert_any_call(D, K2, 0)
        self.cb2.assert_any_call(U, K2, 0)
        self.cb3_up.assert_called_once_with(U, K3, 0)
        self.cb4_1.assert_called_once_with(D, K4, 0)
        self.cb4_2.assert_called_once_with(D, K4, 0)
        self.cb1_again_down.assert_not_called()
        self.cb1_again_up.assert_not_called()

    def test_unregister_cb4_2(self):
        self.unit.unregister_callback(self.cb4_2)
        self.send_keys([K1D, K2D, K3D, K4D, K1U, K2U, K3U, K4U])
        self.cb1_down.assert_called_once_with(D, K1, 0)
        self.cb1_up.assert_called_once_with(U, K1, 0)
        self.cb2.assert_any_call(D, K2, 0)
        self.cb2.assert_any_call(U, K2, 0)
        self.cb3_up.assert_called_once_with(U, K3, 0)
        self.cb4_1.assert_called_once_with(D, K4, 0)
        self.cb4_2.assert_not_called()
        self.cb1_again_down.assert_called_once_with(D, K1, 0)
        self.cb1_again_up.assert_called_once_with(U, K1, 0)

    def test_unregister_cb4_1(self):
        self.unit.unregister_callback(self.cb4_1)
        self.send_keys([K1D, K2D, K3D, K4D, K1U, K2U, K3U, K4U])
        self.cb1_down.assert_called_once_with(D, K1, 0)
        self.cb1_up.assert_called_once_with(U, K1, 0)
        self.cb2.assert_any_call(D, K2, 0)
        self.cb2.assert_any_call(U, K2, 0)
        self.cb3_up.assert_called_once_with(U, K3, 0)
        self.cb4_1.assert_not_called()
        self.cb4_2.assert_called_once_with(D, K4, 0)
        self.cb1_again_down.assert_called_once_with(D, K1, 0)
        self.cb1_again_up.assert_called_once_with(U, K1, 0)

    def test_unregister_after_cb2(self):
        self.unit.unregister_callbacks([
            self.cb3_up,
            self.cb4_1, self.cb4_2,
            self.cb1_again_down, self.cb1_again_up
        ])
        self.send_keys([K1D, K2D, K3D, K4D, K1U, K2U, K3U, K4U])
        self.cb1_down.assert_called_once_with(D, K1, 0)
        self.cb1_up.assert_called_once_with(U, K1, 0)
        self.cb2.assert_any_call(D, K2, 0)
        self.cb2.assert_any_call(U, K2, 0)
        self.cb3_up.assert_not_called()
        self.cb4_1.assert_not_called()
        self.cb4_2.assert_not_called()
        self.cb1_again_down.assert_not_called()
        self.cb1_again_up.assert_not_called()
