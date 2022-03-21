from typing import NamedTuple, Union
from math import pow, sqrt, cos, sin, atan2


_magv2 = lambda a: sqrt(pow(abs(a[0]), 2) + pow(abs(a[1]), 2))


class Vector2(NamedTuple):

    x: float
    y: float

    @staticmethod
    def zero() -> "Vector2":
        return Vector2(0, 0)

    @staticmethod
    def from_rotation(rotation: float, magnitude: float = 1) -> "Vector2":
        return Vector2(
            cos(rotation) * magnitude,
            sin(rotation) * magnitude)

    def __bool__(self) -> bool:
        return self.x != 0 and self.y != 0

    def __repr__(self):
        return f"<Vector2 ({self.x}, {self.y})>"

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __pos__(self):
        return Vector2(+self.x, +self.y)

    def __invert__(self):
        return Vector2(~self.x, ~self.y)

    def __add__(self, other):
        if isinstance(other, Vector2) or isinstance(other, tuple):
            _x, _y = other
            return Vector2(self.x + _x, self.y + _y)
        else:
            return Vector2(self.x + other, self.y + other)

    def __sub__(self, other):
        if isinstance(other, Vector2) or isinstance(other, tuple):
            _x, _y = other
            return Vector2(self.x - _x, self.y - _y)
        else:
            return Vector2(self.x - other, self.y - other)

    def __mul__(self, other):
        if isinstance(other, Vector2) or isinstance(other, tuple):
            return self.dot(other)
        else:
            return Vector2(self.x*other, self.y*other)

    def dot(self, other: "Vector2") -> float:
        _x, _y = other
        x = self.x * _x
        y = self.y * _y
        return x + y

    def magnitude(self) -> float:
        return _magv2(self)

    def dist(self, other: "Vector2") -> float:
        return _magv2(self - other)

    def normalize(self):
        k = self.magnitude()
        if k:
            return Vector2(self.x/k, self.y/k)
        else:
            return Vector2(0, 0)

    def rotate(self, rotation: float) -> None:
        rotation = atan2(self.x, self.y) + rotation
        magnitude = self.magnitude()
        return Vector2.from_rotation(rotation, magnitude)
