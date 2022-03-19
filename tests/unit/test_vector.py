from unittest import TestCase
from airena.vector import Vector2


class Vector2Tests(TestCase):

    def test_add(self):
        v1 = Vector2(5, 3)
        v2 = Vector2(3, 2)
        self.assertEqual(v1 + v2, (8, 5))

    def test_add_scaler(self):
        v1 = Vector2(5, 3)
        self.assertEqual(v1 + 10, (15, 13))

    def test_sub(self):
        v1 = Vector2(5, 3)
        v2 = Vector2(3, 2)
        self.assertEqual(v1 - v2, (2, 1))

    def test_sub_scaler(self):
        v1 = Vector2(5, 3)
        self.assertEqual(v1 - 3, (2, 0))

    def test_dot_product(self):
        v1 = Vector2(-6, 8)
        v2 = Vector2(5, 12)
        self.assertEqual(v1 * v2, 66)

    def test_mul_scaler(self):
        v1 = Vector2(5, 3)
        self.assertEqual(v1 * 10, (50, 30))

    def test_dist_1(self):
        a = Vector2(0, 0)
        b = Vector2(3, 4)
        self.assertEqual(a.dist(b), 5)

    def test_dist_2(self):
        a = Vector2(-3, -4)
        b = Vector2(0, 0)
        self.assertEqual(a.dist(b), 5)

    def test_dist_2(self):
        a = Vector2(3, 4)
        b = Vector2(3, 4)
        self.assertEqual(a.dist(b), 0)

    def test_dist_2(self):
        a = Vector2(3, 4)
        b = Vector2(-3, -4)
        self.assertEqual(a.dist(b), 10)

    def test_normalize_zero(self):
        self.assertEqual(Vector2(0, 0).normalize(), (0, 0))

    def test_normalize(self):
        self.assertEqual(Vector2(3, 4).normalize(), (3/5, 4/5))

    def test_magnitude(self):
        self.assertEqual(Vector2(3, 4).magnitude(), 5)
